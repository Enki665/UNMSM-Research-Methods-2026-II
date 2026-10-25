# Reproducibility Audit and Best Practices (v0.1)

PhD in Deep Tech · UNMSM · Sessions 6–7 · Edgar Aldair Quispe Huaman

## 1. Audited Paper

**Li, X., Ding, Q., & Sun, J.-Q. (2018). Remaining useful life estimation in prognostics using deep convolution neural networks. *Reliability Engineering & System Safety, 172*, 1–11.**

Selected because it is a widely used deep learning reference for remaining-useful-life estimation on the C-MAPSS run-to-failure benchmark (Saxena et al., 2008), the public dataset that this thesis uses to calibrate and validate its fleet simulator.

## 2. Claims Audited

| ID | Claim | Type |
|---|---|---|
| C1 | A one-dimensional convolutional network over sliding windows of sensor data estimates remaining useful life more accurately than earlier data-driven approaches on C-MAPSS. | Quality |
| C2 | The approach does not require prior expertise in prognostics or signal processing. | Usability |

## 3. Documentary Audit

| Criterion | Assessment |
|---|---|
| Dataset public | Yes, C-MAPSS is openly distributed by NASA |
| Preprocessing described | Sensor selection, normalization and time-window construction are described |
| Target definition | Remaining useful life is capped with a piecewise-linear target, an analyst choice that directly affects reported error |
| Code released | Not released with the article; reproduction requires reimplementation |
| Variance across runs | Assessed through the multi-seed reimplementation in section 5 |
| Baselines | Compared with previously published results rather than re-run under identical conditions |

## 4. Threats to Validity Identified

1. **Target construction:** the cap on remaining useful life changes the error scale; comparisons across papers are valid only if the cap is identical.
2. **Normalization leakage:** normalization statistics must be computed on training engines only; computing them over the full dataset leaks test information.
3. **Evaluation point:** C-MAPSS test error is computed at the last observed cycle of each engine, which is not the decision point of a maintenance planner.
4. **Benchmark-to-domain transfer:** turbofan engines in a controlled simulation differ from underground loaders in duty cycles, sensing and connectivity; the benchmark validates method, not mining utility.
5. **Single-run reporting:** without several seeds, differences against baselines cannot be tested statistically.

## 5. Reproduction Plan

Reimplement the convolutional model on the C-MAPSS FD001 subset with normalization fitted on training engines only, the same remaining-useful-life cap, ten seeds and bootstrap 95% confidence intervals for RMSE. The claim is reproduced if the published error falls within the confidence interval of the reimplementation.

## 6. Best Practices Applied to the Own Pipeline

| Practice | Implementation in [05_Reproducible_ML_Pipeline](../05_Reproducible_ML_Pipeline/) |
|---|---|
| Unit of analysis declared | One simulation replication of the fleet under one policy |
| Common random numbers | All policies run on identical degradation, duty, noise and connectivity trajectories |
| Replications | 30 paired replications per scenario |
| Statistical testing | Wilcoxon signed-rank test, rank-biserial effect size, Holm correction |
| Uncertainty | Bootstrap 95% confidence intervals for means and paired differences |
| No leakage | The diagnosis agent learns its healthy baseline only from the warm-up period |
| Unfavorable results reported | The pilot's higher maintenance cost against calendar-based maintenance is reported |
| Pinned environment | requirements.txt and environment logged per run |
| Full configuration logged | One JSON file per experiment with configuration, environment and commit |
| Code and configuration released | This public repository |
