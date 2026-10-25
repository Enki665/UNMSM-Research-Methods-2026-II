# Model Card (v0.1) — following Mitchell et al. (2019)

> Status: **template** for the adapted models produced by the pipeline in [05](../05_Reproducible_ML_Pipeline/). One card per released adapter.

## Model details
- **Developer:** Edgar Aldair Quispe Huaman (UNMSM, PhD in Deep Tech)
- **Base model:** ⏳ (e.g., Qwen/Qwen2.5-0.5B) · **Base model license:** ⏳
- **Adaptation:** LoRA (rank ⏳, target modules ⏳) on a ⏳-bit quantized base
- **Version / date:** ⏳ · **Code commit:** ⏳
- **License of the adapter:** ⏳

## Intended use
- **Primary use:** research on efficient adaptation under limited hardware.
- **Out of scope:** production decisions on people (e.g., electoral, legal or administrative decisions) without further validation.

## Factors
- Language (Spanish vs. English), text domain, quantization level, hardware class.

## Metrics
- Quality: accuracy, macro-F1 (mean ± std over 5 seeds, bootstrap 95% CI)
- Cost: peak memory (GiB), latency (ms/query), energy (Wh)

## Evaluation data
- ⏳ dataset, split, size, preprocessing (see the Datasheet)

## Training data
- ⏳ (see the Datasheet)

## Quantitative analyses
| Configuration | Accuracy | Macro-F1 | Peak mem (GiB) | Latency (ms) | Energy (Wh) |
|---|---|---|---|---|---|
| ⏳ | | | | | |

**Disaggregated results:** ⏳ (e.g., by language or subgroup, to check whether quantization degrades some groups more)

## Ethical considerations
- No personal data in the public benchmarks used. If institutional data is used: Law N° 29733 compliance, anonymization, local-only processing.

## Caveats and recommendations
- Results are hardware-specific; bitsandbytes kernels are not bit-exact deterministic.
