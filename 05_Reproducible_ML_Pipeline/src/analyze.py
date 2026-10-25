"""Aggregate runs across seeds, compute the quality-memory Pareto frontier,
and run a paired comparison between two configurations.

Usage:
    python src/analyze.py
    python src/analyze.py --compare "bits=4,rank=8,target_modules=attn" "bits=4,rank=64,target_modules=all_linear"
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
CONFIG_COLS = ["model", "dataset", "bits", "rank", "target_modules"]
QUALITY = "f1_macro"
COST = "train_peak_mem_gib"


def bootstrap_ci(x, n=2000, alpha=0.05, seed=0):
    x = np.asarray(x, dtype=float)
    if len(x) < 2:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return tuple(np.quantile(means, [alpha / 2, 1 - alpha / 2]))


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for key, g in df.groupby(CONFIG_COLS):
        lo, hi = bootstrap_ci(g[QUALITY])
        rows.append({
            **dict(zip(CONFIG_COLS, key)),
            "n_seeds": len(g),
            f"{QUALITY}_mean": g[QUALITY].mean(),
            f"{QUALITY}_std": g[QUALITY].std(ddof=1),
            f"{QUALITY}_ci_low": lo,
            f"{QUALITY}_ci_high": hi,
            f"{COST}_mean": g[COST].mean(),
            "latency_ms_mean": g["latency_ms_mean"].mean(),
            "train_energy_wh_mean": g["train_energy_wh"].mean(),
        })
    return pd.DataFrame(rows)


def pareto_front(summary: pd.DataFrame) -> pd.DataFrame:
    """Non-dominated configs: maximize quality, minimize memory."""
    q, c = summary[f"{QUALITY}_mean"].values, summary[f"{COST}_mean"].values
    keep = []
    for i in range(len(summary)):
        dominated = np.any((q >= q[i]) & (c <= c[i]) & ((q > q[i]) | (c < c[i])))
        keep.append(not dominated)
    return summary[keep].sort_values(f"{COST}_mean")


def select(df: pd.DataFrame, spec: str) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)
    for part in spec.split(","):
        k, v = part.split("=")
        mask &= df[k].astype(str) == v
    return df[mask]


def paired_compare(df: pd.DataFrame, a: str, b: str) -> None:
    """Paired by seed (same seed = same data order). Wilcoxon signed-rank + effect size."""
    A = select(df, a).set_index("seed")[QUALITY]
    B = select(df, b).set_index("seed")[QUALITY]
    common = A.index.intersection(B.index)
    diff = (A.loc[common] - B.loc[common]).values
    print(f"\nPaired comparison on {QUALITY} over {len(common)} seeds")
    print(f"  A: {a}\n  B: {b}")
    lo, hi = bootstrap_ci(diff)
    print(f"  mean diff (A-B) = {diff.mean():.4f}  bootstrap 95% CI = [{lo:.4f}, {hi:.4f}]")
    if len(common) >= 5 and np.any(diff != 0):
        res = stats.wilcoxon(diff)
        print(f"  Wilcoxon W = {res.statistic:.3f}, p = {res.pvalue:.4f}")
        if len(common) < 6:
            # With n=5 pairs the smallest attainable two-sided p is 0.0625: significance at 0.05 is impossible.
            print("  WARNING: n < 6 paired seeds -> two-sided Wilcoxon cannot reach p < 0.05. "
                  "Pool pairs across tasks/models or use a mixed-effects model.")
    else:
        print("  Too few paired seeds (or no differences) for a Wilcoxon test.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=str(ROOT / "results" / "runs.csv"))
    ap.add_argument("--compare", nargs=2, metavar=("CONFIG_A", "CONFIG_B"))
    args = ap.parse_args()

    df = pd.read_csv(args.runs)
    summary = summarize(df)
    summary.to_csv(ROOT / "results" / "summary.csv", index=False)
    front = pareto_front(summary)
    front.to_csv(ROOT / "results" / "pareto_front.csv", index=False)
    print(summary.to_string(index=False))
    print("\nPareto front (max quality, min training memory):")
    print(front.to_string(index=False))
    if args.compare:
        paired_compare(df, *args.compare)


if __name__ == "__main__":
    main()
