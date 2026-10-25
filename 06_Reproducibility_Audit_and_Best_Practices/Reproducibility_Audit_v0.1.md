# Reproducibility Audit Report (v0.1)

PhD in Deep Tech — UNMSM · Sessions 6–7 · Edgar Aldair Quispe Huaman

> Status: **template**. Fill it in after attempting to reproduce the target paper.

## 1. Audited paper

- **Paper:** ⏳ (suggested: Dettmers et al., 2023, *QLoRA*, NeurIPS — the direct antecedent of the thesis)
- **Claim audited:** ⏳ (one specific, quantitative claim, e.g., "4-bit NF4 + LoRA matches 16-bit full fine-tuning on task X")
- **Artifacts released by the authors:** code ☐ · weights ☐ · data ☐ · configs ☐ · logs ☐

## 2. Reproduction setup

| Item | Original paper | My reproduction |
|---|---|---|
| Model | | |
| Dataset / split | | |
| Hardware | | |
| Library versions | | |
| Hyperparameters | | |
| Seeds (n) | | |

## 3. Results

| Metric | Reported | Reproduced (mean ± std, n seeds) | Within CI? |
|---|---|---|---|
| | | | |

**Verdict:** ☐ Reproduced · ☐ Partially reproduced · ☐ Not reproduced. Explanation: ⏳

## 4. Experimental-practice checklist (Session 6)

| Practice | Original paper | My pipeline (05) |
|---|---|---|
| Train/validation/test split documented, no leakage | ⏳ | ⏳ |
| Multiple seeds; variance reported | ⏳ | ✅ 5 seeds |
| Statistical test for comparisons | ⏳ | ✅ Wilcoxon + bootstrap CI |
| Effect sizes reported | ⏳ | ⏳ |
| Baselines tuned with the same budget | ⏳ | ⏳ |
| Ablations isolate each component | ⏳ | ⏳ |
| Construct validity of the benchmark argued (Bean et al., 2025) | ⏳ | ⏳ |
| Library versions pinned | ⏳ | ✅ requirements.txt + per-run log |
| Hardware and compute cost reported | ⏳ | ✅ memory, latency, energy |
| Code and configs released | ⏳ | ✅ this repository |

## 5. Threats to reproducibility found

1. ⏳
2. ⏳
3. ⏳

## 6. Best practices adopted in my own pipeline as a result

⏳
