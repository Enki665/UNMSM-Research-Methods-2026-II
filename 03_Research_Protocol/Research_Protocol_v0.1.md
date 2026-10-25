# Research Protocol Outline (v0.1)

PhD in Deep Tech · UNMSM · Session 3 · Edgar Aldair Quispe Huaman

## 01 · Title

A budget-aware method for the efficient adaptation of foundation models through quantization and low-rank adaptation on limited computational infrastructure: the case of Peruvian public institutions.

*Método de adaptación eficiente de modelos fundacionales basado en cuantización y ajuste de bajo rango para la mejora del desempeño en infraestructuras computacionales limitadas.*

## 02 · Abstract

Peruvian public institutions that process personal and electoral data must adapt and deploy foundation models locally, because Law N° 29733 restricts sending such data to external cloud services, yet they operate with modest and intermittently available GPU capacity. Parameter-efficient fine-tuning and quantization, combined in QLoRA, make adaptation on a single GPU feasible, but these techniques are proposed and validated in fixed, author-chosen configurations on high-end hardware, leaving practitioners to select quantization precision and adapter rank by trial and error. Grounded in Design Science Research (DSR), this doctoral project designs, builds and evaluates a budget-aware configuration-selection method that, given a memory budget, recommends the quantization precision, adapter rank and target modules that maximize the attainable quality. Evaluation proceeds in two phases: a fractional factorial characterization of the configuration space, replicated over five seeds per configuration, that estimates the quality–memory–latency–energy Pareto frontier; and a confirmatory paired comparison of the proposed method against default LoRA, QLoRA and AdaLoRA configurations on held-out models and Spanish-language tasks. The expected contribution is an improvement-type artifact (Gregor & Hevner, 2013), an empirical trade-off frontier and transferable design principles for resource-constrained adaptation.

## 03 · Introduction & Problem Statement ("So What?" Test)

- **The empirical gap:** full fine-tuning requires storing weights, gradients and optimizer states, which places adaptation out of reach for organizations without high-end GPU clusters. LoRA (Hu et al., 2022), post-training quantization (Dettmers et al., 2022; Frantar et al., 2023; Lin et al., 2024) and their combination in QLoRA (Dettmers et al., 2023) reduce this cost, but they are evaluated in fixed configurations on high-end hardware. There is no systematic characterization of how the quality–cost trade-off varies across the configuration space, nor a formal criterion to select a configuration for a given budget (Ding et al., 2023; Zhu et al., 2024; Mao et al., 2025).
- **Why care ("So What?"):** institutions such as the JNE cannot outsource adaptation to cloud providers for legal reasons and cannot afford exploratory compute. A validated selection method turns adaptation from trial and error into a reproducible decision, enabling local, legally compliant use of foundation models on existing hardware.

## 04 · Literature Review Axes

1. **Parameter-efficient fine-tuning:** adapters (Houlsby et al., 2019), LoRA (Hu et al., 2022), AdaLoRA (Zhang et al., 2023), DoRA (Liu et al., 2024).
2. **Quantization of large models:** LLM.int8() (Dettmers et al., 2022), GPTQ (Frantar et al., 2023), SmoothQuant (Xiao et al., 2023), AWQ (Lin et al., 2024).
3. **Quantization combined with adaptation:** QLoRA (Dettmers et al., 2023) as the immediate antecedent.
4. **Efficiency and sustainability:** Strubell et al. (2019); Schwartz et al. (2020).
5. **Compute-optimal allocation:** scaling laws (Kaplan et al., 2020; Hoffmann et al., 2022), transferred here from pre-training to adaptation.

The systematic review that consolidates these axes is in [04_Literature_Review_PRISMA](../04_Literature_Review_PRISMA/).

## 05 · Research Questions, Objectives & Hypotheses

**General question:** To what extent does a budget-aware adaptation method based on quantization and low-rank adaptation improve performance on limited computational infrastructure, compared with reference adaptation strategies?

**General objective:** Develop and validate a budget-aware adaptation method that improves the quality–cost trade-off on limited infrastructure with respect to reference strategies.

| | Specific question | Specific objective | Hypothesis |
|---|---|---|---|
| SO1 | What is the effect of quantization precision on quality, memory and latency? | Characterize experimentally the effect of quantization precision. | HE1: precision has a significant effect on quality and memory, with a threshold below which degradation is no longer bounded. |
| SO2 | How does the optimal rank and target-module configuration vary with the memory budget? | Determine the functional relation between memory budget and optimal adapter configuration. | HE2: the optimal configuration depends significantly on the memory budget and can be characterized by an allocation function. |
| SO3 | Does automatic configuration selection improve the performance–cost ratio over default configurations? | Design an automatic selection procedure from the empirical characterization. | HE3: the procedure achieves a significantly better performance–cost ratio than default configurations under the same budget. |
| SO4 | Does the method generalize across model families, task domains and hardware classes? | Validate the method against reference strategies on held-out tasks, models and hardware. | HE4: the improvement remains significant across model families, domains and hardware classes. |

**Construct definition:** performance is a vector (quality, peak memory, latency, energy). A configuration improves on another when it Pareto-dominates it; scalar comparisons use quality per GiB of peak memory and quality per Wh.

**Baselines:** LoRA with its original default configuration, QLoRA with its original default configuration, and AdaLoRA.

## 06 · Methodology

- **Paradigm:** Design Science (Hevner et al., 2004), with positivist experimentation as the rigor cycle.
- **Process:** DSR methodology of Peffers et al. (2007): problem identification, objectives, design and development, demonstration, evaluation and communication.
- **Unit of analysis:** the training run, defined as the adaptation of one model under one configuration followed by evaluation on a test set.
- **Phase I, characterization:** fractional factorial design over model family (1B–13B open models), quantization precision (16, 8, 4 and 3 bits), adapter rank (2–64), target modules and task, with five seeds per configuration and randomized execution order. Response-surface methodology and Pareto-frontier analysis.
- **Phase II, confirmatory evaluation:** the selection method against the baselines on tasks and models not used in Phase I, under identical memory budgets.
- **Statistical analysis:** paired comparisons across seeds, tasks and models using linear mixed-effects models (seed and task as random effects) and the Wilcoxon signed-rank test on pooled pairs, with bootstrap 95% confidence intervals, effect sizes and Holm correction for multiple comparisons. Because five paired seeds alone cannot reach p < 0.05 in a two-sided Wilcoxon test, inference pools pairs across tasks and models.
- **Measurement:** accuracy, macro-F1 and perplexity; peak memory during training and inference (GiB); latency per query after warm-up (ms); throughput (tokens/s); energy from GPU telemetry (Wh).
- **Reproducibility:** pinned library versions, fixed seeds, full configuration and environment logged per run, public code in [05_Reproducible_ML_Pipeline](../05_Reproducible_ML_Pipeline/).

## 07 · Ethics, Governance & Data Protection

- **Scientific integrity:** compliance with CONCYTEC's National Code of Scientific Integrity; pre-specified hypotheses and analysis plan to prevent p-hacking, HARKing and selective reporting; all runs reported, including failed ones.
- **Data protection:** Phases I and II use open models and public benchmarks without personal data. Any institutional data is processed only with written authorization, anonymized before analysis, processed locally, and handled under Law N° 29733 and its Regulation.
- **AI regulation:** alignment with Law N° 31814, which promotes the use of artificial intelligence in Peru, and its Regulation.
- **Fairness:** disaggregated evaluation to test whether low-bit quantization degrades Spanish-language performance more than English performance.
- **Sustainability:** energy consumption reported as an outcome variable.
- **AI-use declaration:** generative AI was used for structuring, preliminary drafting and code scaffolding; methodological decisions are the author's own.

## 08 · Expected Results

1. A validated budget-aware configuration-selection method released as open-source software.
2. An empirical quality–memory–latency–energy Pareto frontier for quantized low-rank adaptation on limited hardware.
3. Transferable design principles for resource-constrained adaptation, published in target venues (MLSys, TMLR, EMNLP Findings).

## 09 · Timeline & Budget

| Activity | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---|---|---|---|---|---|---|---|---|
| Systematic literature review | X | X | | | | | | |
| Project formulation and approval | X | X | | | | | | |
| Experimental environment | | X | X | | | | | |
| Phase I: characterization | | | X | X | | | | |
| Phase I statistical analysis | | | | X | X | | | |
| First paper | | | | | X | | | |
| Design of the selection method | | | | | X | X | | |
| Phase II: confirmatory validation | | | | | | X | X | |
| Second paper | | | | | | | X | |
| Thesis writing | | | | | | | X | X |
| Defense | | | | | | | | X |

- **Risk buffer:** GPU availability, slower-than-planned Phase I and ethics approval if institutional data is added.
- **Budget:** S/ 47,520 (workstation, cloud compute, storage, bibliography, dissemination, editing and a 10% contingency), financed through UNMSM competitive funds and national science and technology calls.

## 10 · Core Bibliography

- Dettmers, T., Lewis, M., Belkada, Y., & Zettlemoyer, L. (2022). LLM.int8(): 8-bit matrix multiplication for transformers at scale. *NeurIPS 35*.
- Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA: Efficient finetuning of quantized LLMs. *NeurIPS 36*.
- Ding, N., et al. (2023). Parameter-efficient fine-tuning of large-scale pre-trained language models. *Nature Machine Intelligence, 5*(3), 220–235.
- Frantar, E., Ashkboos, S., Hoefler, T., & Alistarh, D. (2023). GPTQ: Accurate post-training quantization for generative pre-trained transformers. *ICLR 2023*.
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105.
- Hoffmann, J., et al. (2022). Training compute-optimal large language models. *arXiv:2203.15556*.
- Houlsby, N., et al. (2019). Parameter-efficient transfer learning for NLP. *ICML 2019*, 2790–2799.
- Hu, E. J., et al. (2022). LoRA: Low-rank adaptation of large language models. *ICLR 2022*.
- Kaplan, J., et al. (2020). Scaling laws for neural language models. *arXiv:2001.08361*.
- Lin, J., et al. (2024). AWQ: Activation-aware weight quantization for on-device LLM compression and acceleration. *MLSys 2024*.
- Liu, S.-Y., et al. (2024). DoRA: Weight-decomposed low-rank adaptation. *ICML 2024*.
- Mao, Y., et al. (2025). A survey on LoRA of large language models. *Frontiers of Computer Science, 19*(7), 197605.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77.
- Schwartz, R., Dodge, J., Smith, N. A., & Etzioni, O. (2020). Green AI. *Communications of the ACM, 63*(12), 54–63.
- Strubell, E., Ganesh, A., & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. *ACL 2019*, 3645–3650.
- Xiao, G., et al. (2023). SmoothQuant: Accurate and efficient post-training quantization for large language models. *ICML 2023*.
- Zhang, Q., et al. (2023). AdaLoRA: Adaptive budget allocation for parameter-efficient fine-tuning. *ICLR 2023*.
- Zhu, X., Li, J., Liu, Y., Ma, C., & Wang, W. (2024). A survey on model compression for large language models. *TACL, 12*, 1556–1577.
