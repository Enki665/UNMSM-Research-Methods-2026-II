# Datasheet for Datasets (v0.1)

PhD in Deep Tech · UNMSM · Session 7 · Edgar Aldair Quispe Huaman · Format: Gebru et al. (2021)

**Dataset:** SST-2 (Stanford Sentiment Treebank, binary version), distributed in the GLUE benchmark (Hugging Face: `nyu-mll/glue`, subset `sst2`).

## Motivation

Created as a benchmark for sentence-level sentiment classification (Socher et al., 2013) and included in GLUE (Wang et al., 2018). In this project it validates the reproducible pipeline before the Spanish-language experiments.

## Composition

| Field | Value |
|---|---|
| Instance | One English sentence from a movie review |
| Label | Binary sentiment: negative (0) or positive (1) |
| Splits | Train 67,349 · Validation 872 · Test 1,821 (test labels not public) |
| Personal data | None |

## Collection Process

Sentences were extracted from movie reviews on Rotten Tomatoes (Pang & Lee, 2005) and labeled for sentiment through crowdsourcing (Socher et al., 2013).

## Preprocessing in This Project

Tokenization with the base model tokenizer, truncation to 128 tokens and random subsampling with a fixed seed: 500 training sentences and 200 validation sentences in the smoke configuration.

## Uses

- **Use in this project:** validation of the training, measurement and logging pipeline.
- **Limitation:** English movie-review text does not represent Spanish institutional text, so it is not used to support the thesis hypotheses.

## Distribution and Maintenance

Distributed through the GLUE benchmark and the Hugging Face Hub; the exact dataset revision is recorded in each run log.

## Legal Compliance (Peru)

Contains no personal data within the scope of Law N° 29733.

## References

- Pang, B., & Lee, L. (2005). Seeing stars: Exploiting class relationships for sentiment categorization with respect to rating scales. *ACL 2005*.
- Socher, R., et al. (2013). Recursive deep models for semantic compositionality over a sentiment treebank. *EMNLP 2013*.
- Wang, A., et al. (2018). GLUE: A multi-task benchmark and analysis platform for natural language understanding. *BlackboxNLP Workshop, EMNLP 2018*.
