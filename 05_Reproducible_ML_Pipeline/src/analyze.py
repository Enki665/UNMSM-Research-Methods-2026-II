from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
METRICS = {
    "availability": "higher",
    "unplanned_failures": "lower",
    "maintenance_cost": "lower",
    "unnecessary_interventions": "lower",
}
POLICY_ORDER = ["reactive", "preventive", "twin_agent"]


def bootstrap_ci(x, n=5000, alpha=0.05, seed=0):
    x = np.asarray(x, dtype=float)
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return lo, hi


def rank_biserial(diff: np.ndarray) -> float:
    d = diff[diff != 0]
    if len(d) == 0:
        return 0.0
    ranks = stats.rankdata(np.abs(d))
    return float((ranks[d > 0].sum() - ranks[d < 0].sum()) / ranks.sum())


def holm(pvalues: list[float]) -> list[float]:
    m = len(pvalues)
    order = np.argsort(pvalues)
    adjusted = np.empty(m)
    running = 0.0
    for i, idx in enumerate(order):
        running = max(running, (m - i) * pvalues[idx])
        adjusted[idx] = min(running, 1.0)
    return adjusted.tolist()


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for policy in POLICY_ORDER:
        g = df[df.policy == policy]
        for metric in METRICS:
            lo, hi = bootstrap_ci(g[metric])
            rows.append({"policy": policy, "metric": metric, "mean": g[metric].mean(),
                         "sd": g[metric].std(ddof=1), "ci95_low": lo, "ci95_high": hi, "n": len(g)})
    return pd.DataFrame(rows)


def paired_tests(df: pd.DataFrame) -> pd.DataFrame:
    wide = {p: df[df.policy == p].set_index("replication") for p in POLICY_ORDER}
    rows = []
    for baseline in ["reactive", "preventive"]:
        for metric in METRICS:
            diff = (wide["twin_agent"][metric] - wide[baseline][metric]).values
            p = stats.wilcoxon(diff).pvalue if np.any(diff != 0) else 1.0
            lo, hi = bootstrap_ci(diff)
            rows.append({"comparison": f"twin_agent vs {baseline}", "metric": metric,
                         "mean_diff": diff.mean(), "ci95_low": lo, "ci95_high": hi,
                         "rank_biserial": rank_biserial(diff), "p_value": p})
    out = pd.DataFrame(rows)
    out["p_holm"] = holm(out["p_value"].tolist())
    return out


def plot(df: pd.DataFrame, name: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, metric in zip(axes, ["availability", "unplanned_failures", "maintenance_cost"]):
        data = [df[df.policy == p][metric].values for p in POLICY_ORDER]
        ax.boxplot(data)
        ax.set_xticks(range(1, len(POLICY_ORDER) + 1), POLICY_ORDER)
        ax.set_title(metric)
        ax.grid(alpha=0.3)
    fig.suptitle(f"Pilot simulation · {df.replication.nunique()} paired replications")
    fig.tight_layout()
    fig.savefig(RESULTS / f"{name}_boxplots.png", dpi=150)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", default="pilot_lhd_fleet")
    args = ap.parse_args()
    df = pd.read_csv(RESULTS / f"runs_{args.experiment}.csv")
    summary = summarize(df)
    tests = paired_tests(df)
    summary.to_csv(RESULTS / f"summary_{args.experiment}.csv", index=False)
    tests.to_csv(RESULTS / f"paired_tests_{args.experiment}.csv", index=False)
    plot(df, args.experiment)
    print(summary.round(4).to_string(index=False))
    print()
    print(tests.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
