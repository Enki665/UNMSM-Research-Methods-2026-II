# Reproducibility Audit and Best Practices (v0.1)

PhD in Deep Tech · UNMSM · Sessions 6–7 · Edgar Aldair Quispe Huaman

## 1. Audited Paper

**Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient finetuning of quantized LLMs. NeurIPS 36.**

Selected because it is the immediate antecedent of the thesis: it combines 4-bit quantization of a frozen base model with low-rank adapters.

## 2. Claims Audited

| ID | Claim | Type |
|---|---|---|
| C1 | A 65B-parameter model can be fine-tuned on a single 48 GB GPU. | Cost |
| C2 | 4-bit NormalFloat (NF4) with double quantization preserves the performance of 16-bit fine-tuning. | Quality |
| C3 | The resulting Guanaco models are competitive with ChatGPT on the Vicuna benchmark. | Quality |

## 3. Documentary Audit

| Criterion | Assessment |
|---|---|
| Code released | Yes, public repository with training scripts |
| Trained adapters released | Yes, Guanaco adapters on Hugging Face |
| Hardware reported | Yes, single-GPU memory requirements |
| Datasets identified | Yes, public instruction-tuning datasets |
| Evaluation instrument | C3 relies on GPT-4 as judge and on Elo tournaments, an LLM used as a measurement instrument |
| Reproducibility risk | High for C3: the judge model is non-deterministic and its version changes over time, so the instrument cannot be pinned; low to medium for C1 and C2, which rely on deterministic metrics and released code |

## 4. Threats to Validity Identified

1. **LLM as instrument (C3):** construct validity, reliability without validity, non-determinism and versioning, and circularity apply to GPT-4-as-judge evaluation, as discussed in Session 2.
2. **Hardware dependence (C1):** the memory claim depends on paged optimizers and on the specific GPU; it does not transfer automatically to consumer GPUs with less memory.
3. **Configuration choice:** precision, rank and target modules are fixed by the authors; the paper does not characterize how quality varies across the configuration space under different budgets, which is the gap addressed by this thesis.

## 5. Reproduction Plan

Reproduction of C2 at reduced scale: Qwen2.5-0.5B adapted with LoRA under 16-bit, 8-bit and 4-bit NF4, five seeds per configuration, comparing macro-F1 and peak memory with the pipeline in [05_Reproducible_ML_Pipeline](../05_Reproducible_ML_Pipeline/). The claim is reproduced if the 4-bit configuration falls within the 95% bootstrap confidence interval of the 16-bit configuration.

## 6. Best Practices Applied to the Own Pipeline

| Practice | Implementation |
|---|---|
| Unit of analysis declared | The training run |
| Multiple seeds | Five seeds per configuration |
| Variance reported | Mean, standard deviation and bootstrap 95% confidence interval |
| Statistical testing | Paired Wilcoxon signed-rank test and pooled comparisons |
| Randomized execution order | Fixed shuffle seed for the grid |
| Pinned environment | requirements.txt and library versions logged per run |
| Full configuration logged | One JSON file per run with configuration, environment and metrics |
| Cost reported | Peak memory, latency and energy per run |
| Failed runs reported | Out-of-memory and other failures logged as data |
| Code and configuration released | This public repository |
