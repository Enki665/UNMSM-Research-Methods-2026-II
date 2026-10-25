# Research Paradigm Justification Statement (v1.0)

PhD in Deep Tech — UNMSM · Session 1 · Edgar Aldair Quispe Huaman

## 1. Topic and context

Peruvian public institutions that process personal or electoral data, such as the Jurado Nacional de Elecciones (JNE), cannot send that data to external cloud LLM services: Law N° 29733 restricts its processing, so foundation models must be adapted and deployed locally. These institutions typically have modest, intermittently available GPU capacity, far below the infrastructure on which QLoRA-style methods were proposed and validated. Practitioners therefore choose quantization precision and adapter rank by trial and error, wasting scarce compute and often reaching suboptimal configurations.

<!-- TODO: name the actual hardware available (GPU model, VRAM) to make the context concrete. -->

## 2. Research question

How can a configuration-selection method for efficient adaptation (quantization + low-rank adaptation) be designed so that, given a fixed memory budget on limited hardware, it reaches a better quality–cost trade-off than the default configurations used in the literature, and how transferable are its design principles across model families, Spanish-language tasks and hardware classes?

## 3. Paradigm and justification

I adopt **Design Science** (Hevner et al., 2004): the contribution is an artifact, a budget-aware selection method, together with its design principles. In Gregor & Hevner's (2013) terms it is an *improvement*: a new solution to a known problem. I do not adopt **positivism** as the governing paradigm; I borrow its controlled factorial experiments as the rigor cycle that evaluates the artifact, so positivism produces my evidence, not my contribution. I reject **interpretivism** because the core problem is computational performance under resource constraints, not the meaning practitioners give to it. I reject **mixed methods** because a qualitative strand would not be integrated into the central claim; it would be appended, producing two weak studies rather than one finding neither could reach alone.

## 4. Implications

- **(a) Data:** experimental runs (model × quantization × rank × target modules × seed), with quality, peak memory, latency and energy logged per run.
- **(b) Methods:** build–evaluate cycles: a fractional factorial characterization, construction of the selection method, then confirmatory paired comparisons on held-out tasks and models, with five seeds per configuration because the unit of analysis is the training run.
- **(c) Contribution:** the selection artifact, an empirical quality–cost Pareto frontier, and reusable design principles.
- **(d) Target venues:** MLSys, TMLR, EMNLP (Findings).

## 5. One doubt or tension

My strongest tension is generalization across hardware classes. My budget gives me one mid-range local GPU plus cloud credits, so "hardware class" may collapse to two or three points, too few to support HE4 statistically. I am considering narrowing that claim to memory budgets simulated on the same device, and stating physical-hardware generalization as a limitation.

## References

- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105.
