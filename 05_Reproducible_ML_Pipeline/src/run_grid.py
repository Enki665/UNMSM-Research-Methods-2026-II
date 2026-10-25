"""Expand a grid of configurations x seeds and run each as an independent run.

Usage:
    python src/run_grid.py --grid configs/grid_phase1.yaml            # run everything
    python src/run_grid.py --grid configs/grid_phase1.yaml --dry-run  # only list the runs
"""
from __future__ import annotations

import argparse
import itertools
import random
import traceback

import yaml

from run_experiment import ROOT, apply_overrides, load_config, run


def expand(grid_cfg: dict) -> list[list[str]]:
    keys = list(grid_cfg["grid"])
    combos = itertools.product(*(grid_cfg["grid"][k] for k in keys))
    runs = []
    for combo in combos:
        for seed in grid_cfg["seeds"]:
            runs.append([f"{k}={v}" for k, v in zip(keys, combo)] + [f"seed={seed}"])
    if grid_cfg.get("shuffle_order", True):
        random.Random(grid_cfg.get("shuffle_seed", 0)).shuffle(runs)
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.grid, encoding="utf-8") as f:
        grid_cfg = yaml.safe_load(f)
    base = load_config(ROOT / grid_cfg["base_config"])
    runs = expand(grid_cfg)
    print(f"{len(runs)} runs planned")

    for i, overrides in enumerate(runs, 1):
        print(f"[{i}/{len(runs)}] {' '.join(overrides)}")
        if args.dry_run:
            continue
        try:
            run(apply_overrides(base, overrides))
        except Exception:
            # Log and continue: a failed run (e.g., OOM) is itself a data point about the budget.
            traceback.print_exc()
            with open(ROOT / "results" / "failed_runs.log", "a", encoding="utf-8") as f:
                f.write(" ".join(overrides) + "\n")


if __name__ == "__main__":
    main()
