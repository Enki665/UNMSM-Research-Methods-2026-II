# 05_Reproducible_ML_Pipeline

Pipeline reproducible para la fase de caracterización de la tesis: adapta un modelo fundacional con cuantización (16, 8 y 4 bits) y LoRA bajo una configuración determinada, y registra la calidad y el costo computacional de cada corrida.

## Principios de diseño

- **Unidad de análisis:** la corrida de entrenamiento; cada configuración se repite con cinco semillas.
- **Trazabilidad:** cada corrida guarda su configuración completa, versiones de bibliotecas, GPU y commit en `results/runs/<run_id>.json`, y una fila en `results/runs.csv`.
- **Orden aleatorizado:** la grilla se ejecuta en orden aleatorio con semilla fija para controlar la deriva térmica.
- **Corridas fallidas:** los errores por falta de memoria se registran en `results/failed_runs.log` como dato del presupuesto.
- **Análisis:** media, desviación estándar e intervalo de confianza bootstrap al 95% por configuración, frontera de Pareto calidad–memoria y prueba pareada de Wilcoxon.

## Estructura

```
05_Reproducible_ML_Pipeline/
├── configs/
│   ├── smoke.yaml
│   └── grid_phase1.yaml
├── src/
│   ├── run_experiment.py
│   ├── run_grid.py
│   └── analyze.py
├── results/
└── requirements.txt
```

## Ejecución en Google Colab

```bash
!git clone https://github.com/<usuario>/UNMSM-Research-Methods-2026-II.git
%cd UNMSM-Research-Methods-2026-II/05_Reproducible_ML_Pipeline
!pip install -q -r requirements.txt
!python src/run_experiment.py --config configs/smoke.yaml
!python src/run_experiment.py --config configs/smoke.yaml --set adaptation.bits=8 adaptation.rank=32 seed=22
!python src/run_grid.py --grid configs/grid_phase1.yaml --dry-run
!python src/run_grid.py --grid configs/grid_phase1.yaml
!python src/analyze.py --compare "bits=4,rank=8,target_modules=attn" "bits=4,rank=64,target_modules=all_linear"
```

## Métricas registradas

| Dimensión | Indicador |
|---|---|
| Calidad | Exactitud y F1 macro |
| Memoria | Memoria máxima en entrenamiento e inferencia (GiB) |
| Tiempo | Latencia por consulta (ms) y tiempo de entrenamiento (s) |
| Energía | Energía de entrenamiento y evaluación (Wh) mediante telemetría NVML |
