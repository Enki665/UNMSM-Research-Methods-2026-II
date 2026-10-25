# 05 — Reproducible ML Pipeline

Pipeline for the Phase I characterization of the thesis: adapt a foundation model with **quantization (16/8/4-bit) + LoRA** under one configuration, then log **quality and cost** for that run.

> Status: **code skeleton, not yet executed.** The smoke test must be run before any result is reported.

## Design decisions (from Sessions 1–2)

- **Unit of analysis = training run.** Every configuration is repeated with **5 seeds**, so n > 1 and statistical tests are possible.
- **Everything is logged per run:** full config, library versions, GPU, git commit → `results/runs/<run_id>.json`, plus one row in `results/runs.csv`.
- **Execution order is randomized** (`shuffle_order`) to control thermal drift.
- **Failed runs (e.g., OOM) are logged, not hidden** → `results/failed_runs.log`. Under a memory budget, failure is data.
- **Analysis** reports mean, std and a bootstrap 95% CI per configuration, the quality–memory Pareto frontier, and a paired Wilcoxon test across seeds.

## Structure

```
05_Reproducible_ML_Pipeline/
├── configs/
│   ├── smoke.yaml          # one small run to verify the pipeline
│   └── grid_phase1.yaml    # factorial grid x seeds
├── src/
│   ├── run_experiment.py   # one run: train → evaluate → measure memory, latency, energy
│   ├── run_grid.py         # expand the grid, randomize order, run all
│   └── analyze.py          # aggregate, Pareto frontier, paired tests
├── results/                # generated (git-ignored, except summaries you choose to commit)
└── requirements.txt        # pinned versions
```

## How to run (Google Colab, T4 GPU)

```bash
!git clone https://github.com/<your-user>/UNMSM-Research-Methods-2026-II.git
%cd UNMSM-Research-Methods-2026-II/05_Reproducible_ML_Pipeline
!pip install -q -r requirements.txt

# 1. Smoke test (a few minutes)
!python src/run_experiment.py --config configs/smoke.yaml

# 2. Override a single factor
!python src/run_experiment.py --config configs/smoke.yaml --set adaptation.bits=8 adaptation.rank=32 seed=22

# 3. Plan the grid without running it
!python src/run_grid.py --grid configs/grid_phase1.yaml --dry-run

# 4. Run the grid, then analyze
!python src/run_grid.py --grid configs/grid_phase1.yaml
!python src/analyze.py --compare "bits=4,rank=8,target_modules=attn" "bits=4,rank=64,target_modules=all_linear"
```

Note: Colab ships its own `torch`. If installing the pinned version causes conflicts, keep Colab's torch and **record the version actually used**; it is already logged automatically in each run's JSON.

## Known limitations / TODO

- [ ] Replace the smoke dataset (SST-2, English) with a **Spanish-language task** for the thesis.
- [ ] 3-bit quantization needs a GPTQ/AWQ backend (bitsandbytes supports 4/8 only).
- [ ] Replace the full factorial with a **fractional factorial** design before scaling.
- [ ] Energy uses the NVML counter (Volta+ GPUs); on older GPUs it is logged as empty.
- [ ] bitsandbytes kernels are not bit-exact deterministic; report run-to-run variance instead of claiming exact replication.
