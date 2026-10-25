# Model Card (v0.1)

PhD in Deep Tech · UNMSM · Session 7 · Edgar Aldair Quispe Huaman · Format: Mitchell et al. (2019)

## Model Details

| Field | Value |
|---|---|
| Developer | Edgar Aldair Quispe Huaman, PhD in Deep Tech, UNMSM |
| Base model | Qwen/Qwen2.5-0.5B (Apache 2.0) |
| Adaptation | LoRA adapters trained on a base model quantized at 16, 8 or 4 bits (NF4) |
| Configurations | Rank 2–64; target modules: attention projections or all linear layers |
| Task | Binary sentence classification (pipeline validation stage) |
| Code | [05_Reproducible_ML_Pipeline](../05_Reproducible_ML_Pipeline/) |

## Intended Use

- **Primary use:** research on the quality–cost trade-off of efficient adaptation under limited hardware.
- **Out of scope:** automated decisions about people, including electoral, legal or administrative decisions.

## Factors

Quantization precision, adapter rank, target modules, language of the task and hardware class.

## Metrics

- **Quality:** accuracy and macro-F1, reported as mean ± standard deviation over five seeds with bootstrap 95% confidence intervals.
- **Cost:** peak memory during training and inference (GiB), latency per query (ms) and energy (Wh).

## Evaluation and Training Data

SST-2 (GLUE) for pipeline validation; Spanish-language tasks in the thesis experiments. See [Datasheet_v0.1.md](Datasheet_v0.1.md).

## Ethical Considerations

The validation data contains no personal data. Any institutional data is processed locally, anonymized and handled under Law N° 29733.

## Caveats and Recommendations

Results depend on the hardware used. bitsandbytes kernels are not bit-exact deterministic, so the run-to-run variance is reported instead of exact replication.
