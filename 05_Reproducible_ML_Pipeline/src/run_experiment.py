from __future__ import annotations

import argparse
import copy
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from simulator import generate_exogenous, simulate

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
POLICIES = ["reactive", "preventive", "twin_agent"]


def load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def apply_overrides(cfg: dict, overrides: list[str]) -> dict:
    cfg = copy.deepcopy(cfg)
    for item in overrides:
        key, raw = item.split("=", 1)
        node = cfg
        parts = key.split(".")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = yaml.safe_load(raw)
    return cfg


def environment() -> dict:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        commit = None
    return {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "git_commit": commit}


def run(cfg: dict) -> pd.DataFrame:
    rows = []
    for r in range(cfg["replications"]):
        seed = cfg["base_seed"] + r
        exo = generate_exogenous(cfg, seed)
        for policy in POLICIES:
            rows.append({"replication": r, "seed": seed, "policy": policy, **simulate(cfg, exo, policy)})
    df = pd.DataFrame(rows)
    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}"
    df.to_csv(RESULTS / f"runs_{cfg['experiment']}.csv", index=False)
    with open(RESULTS / f"run_{cfg['experiment']}_{stamp}.json", "w", encoding="utf-8") as f:
        json.dump({"config": cfg, "environment": environment(), "n_rows": len(df)}, f, indent=2)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--set", nargs="*", default=[])
    args = ap.parse_args()
    df = run(apply_overrides(load_config(args.config), args.set))
    print(df.groupby("policy").mean(numeric_only=True).drop(columns=["replication", "seed"]).round(3).to_string())


if __name__ == "__main__":
    main()
