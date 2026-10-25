# Research Protocol v0.1

PhD in Deep Tech — UNMSM · Session 3 · Edgar Aldair Quispe Huaman
Source document: *Propuesta de proyecto de investigación* (UNMSM format, Spanish). This protocol reorganizes it into the course's 10 components and incorporates the corrections from Sessions 1–2.

> Status legend: ✅ adapted from the proposal · ✏️ rewritten after course feedback · ⏳ TODO

---

## 1. Title ✅

**ES:** Método de adaptación eficiente de modelos fundacionales basado en cuantización y ajuste de bajo rango para la mejora del desempeño en infraestructuras computacionales limitadas.
**EN:** A quantization- and low-rank-adaptation-based method for the efficient adaptation of foundation models to improve performance on limited computational infrastructure.

## 2. Abstract ⏳

<!-- TODO (≤250 words): problem → gap → artifact → evaluation design → expected contribution. Write it last. -->

## 3. Problem statement ✅ ✏️

Full fine-tuning of foundation models requires storing weights, gradients and optimizer states, placing adaptation out of reach for organizations without high-end GPU clusters. In domains where data is sensitive or legally restricted (public administration, health, justice, elections), sending data to external services is legally problematic, so **local deployment becomes a requirement that collides with limited infrastructure**.

Parameter-efficient fine-tuning (LoRA; Hu et al., 2022) and quantization (Dettmers et al., 2022; Frantar et al., 2023; Lin et al., 2024), combined in QLoRA (Dettmers et al., 2023), make adaptation on a single GPU possible. However, these techniques are evaluated in **fixed, author-chosen configurations on high-end hardware**. There is no systematic characterization of how the quality–memory–latency–energy trade-off varies across the configuration space, and no formal criterion to select quantization precision and adapter rank for a given compute budget. Practitioners proceed by trial and error.

**Peruvian context ✏️:** institutions such as the JNE process personal and electoral data subject to Law N° 29733 and must adapt models locally on modest hardware. <!-- TODO: name the concrete hardware and one concrete Spanish-language task from the institution (e.g., classification of electoral resolutions) to pass the "remove the country name" test. -->

**"So what?" (30 seconds) ⏳:** <!-- TODO -->

## 4. Literature review ✅ ⏳

Narrative antecedents (from the proposal): Houlsby et al. (2019) adapters; Hu et al. (2022) LoRA; Dettmers et al. (2022) LLM.int8(); Frantar et al. (2023) GPTQ; Lin et al. (2024) AWQ; Dettmers et al. (2023) QLoRA; Zhang et al. (2023) AdaLoRA; Liu et al. (2024) DoRA; surveys by Ding et al. (2023), Zhu et al. (2024), Mao et al. (2025).

**Gap:** mature quantization and low-rank techniques exist and their combination is viable, but there is no systematic characterization of the configuration space nor a procedure to select configurations according to the available compute budget.

⏳ To be replaced by the systematic review in [04_Literature_Review_PRISMA](../04_Literature_Review_PRISMA/).

## 5. Research questions and hypotheses ✅

**General question:** To what extent does an efficient adaptation method based on quantization and low-rank adaptation improve performance on limited computational infrastructure, compared with reference adaptation strategies?

| | Question | Hypothesis |
|---|---|---|
| 1 | Effect of quantization precision on quality, memory and latency? | HE1: precision has a significant effect on quality and memory, with a threshold below which degradation is no longer bounded. |
| 2 | How does the optimal rank / target-module configuration vary with the memory budget? | HE2: the optimal configuration depends significantly on the memory budget, and the dependence can be characterized by an allocation function. |
| 3 | Does automatic configuration selection improve the performance–cost ratio over default configurations? | HE3: the proposed procedure achieves a significantly better performance–cost ratio than defaults under the same budget. |
| 4 | Does the method generalize across model family, task domain and hardware class? | HE4: the improvement remains significant across model families, domains and hardware classes. |

✏️ **Construct definition (required):** "performance" is a vector (quality, peak memory, latency, energy). A configuration *improves* on another when it **Pareto-dominates** it, or, for single-number comparisons, by **quality per GiB** and **quality per Wh**. <!-- TODO: choose and justify one primary metric. -->

✏️ **Baselines (must be named):** (i) LoRA with the original defaults (r = 8, attention projections only); (ii) QLoRA defaults (NF4, r = 64, all linear layers); (iii) AdaLoRA. <!-- TODO: verify default values against the original papers before citing. -->

## 6. Methods ✏️

- **Paradigm:** Design Science (Hevner et al., 2004), with positivist experimentation as the rigor cycle. See [01](../01_Paradigm_Justification/).
- **Method:** DSR following Peffers et al. (2007): problem identification → objectives → design & development → demonstration → evaluation → communication. See [02](../02_Method_Fit_Matrix/).
- **Phase I (characterization):** fractional factorial design over {model family, quantization 16/8/4/3 bits, rank 2–64, target modules, task}. Five seeds per configuration. Response-surface methodology and Pareto-frontier analysis.
- **Phase II (confirmatory):** the selection method vs. baselines on **held-out tasks and models**; run order randomized.
- **Unit of analysis:** the training run (model adapted under one configuration + evaluated on a test set).
- **Statistics ✏️:** paired comparisons across seeds and tasks using the Wilcoxon signed-rank test or linear mixed-effects models (seed and task as random effects), with bootstrap confidence intervals and effect sizes. Holm or Bonferroni correction for multiple comparisons. McNemar is used only as a *complementary* per-run test on shared test instances, since on its own it ignores seed variance.
- **Power caveat ✏️:** with only 5 paired seeds, a two-sided Wilcoxon test can never reach p < 0.05 (its minimum p is 0.0625). Comparisons must therefore pool pairs across tasks and models, use a mixed-effects model, or raise the number of seeds. The power analysis must account for this.
- **Measurement:** quality (accuracy/F1, perplexity), peak memory (training and inference, GiB), latency (ms per query, after warm-up), throughput (tokens/s), energy (Wh, via GPU telemetry).
- **Reproducibility:** pinned library versions, fixed seeds, full configuration logged per run, code in [05](../05_Reproducible_ML_Pipeline/).
- **Note on 3-bit:** bitsandbytes supports 4/8-bit only; 3-bit requires GPTQ or AWQ. <!-- TODO: decide the quantization backend per precision level. -->

## 7. Ethics and data management ⏳ ✏️

- Phase I/II use **open models and public benchmarks**; no personal data is processed.
- If institutional data (e.g., JNE) is added: written authorization, anonymization before processing, local-only processing, compliance with Law N° 29733 and its regulation, and a data management plan aligned with FAIR and CONCYTEC guidance.
- **Bias angle (to be developed in Unit III):** check whether low-bit quantization degrades Spanish-language performance more than English performance.
- Energy reporting as a sustainability commitment (Strubell et al., 2019; Schwartz et al., 2020).

## 8. Expected results ⏳

<!-- TODO: expected Pareto frontier shape, expected precision threshold (HE1), expected form of the allocation function (HE2), what result would falsify each hypothesis. -->

## 9. Timeline ✅

| Activity | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---|---|---|---|---|---|---|---|---|
| Systematic literature review | X | X | | | | | | |
| Project formulation and approval | X | X | | | | | | |
| Experimental environment | | X | X | | | | | |
| Phase I: characterization | | | X | X | | | | |
| Phase I statistical analysis | | | | X | X | | | |
| First paper | | | | | X | | | |
| Design of selection method | | | | | X | X | | |
| Phase II: confirmatory validation | | | | | | X | X | |
| Second paper | | | | | | | X | |
| Thesis writing | | | | | | | X | X |
| Defense | | | | | | | | X |

⏳ Risks to include (Session 3): GPU availability, ethics approval time if institutional data is used, and a slower-than-planned Phase I.

**Budget:** S/ 47,520 (see the proposal).

## 10. Bibliography

See the proposal's reference list. Additions from the course: Gregor & Hevner (2013); Peffers et al. (2007); Bean et al. (2025), *Measuring What Matters* (NeurIPS 2025).
