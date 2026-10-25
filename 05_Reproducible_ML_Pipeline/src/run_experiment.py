"""Run ONE experimental run: adapt a model under one configuration, evaluate it,
and log quality + cost metrics. The run is the unit of analysis.

Usage:
    python src/run_experiment.py --config configs/smoke.yaml
    python src/run_experiment.py --config configs/smoke.yaml --set adaptation.rank=16 seed=22
"""
from __future__ import annotations

import argparse
import copy
import csv
import json
import os
import platform
import random
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

TARGET_MODULE_PRESETS = {
    "attn": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "mlp": ["gate_proj", "up_proj", "down_proj"],
    "all_linear": "all-linear",
}


# --------------------------------------------------------------------------- config
def load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_by_path(cfg: dict, dotted: str, value) -> None:
    keys = dotted.split(".")
    node = cfg
    for k in keys[:-1]:
        node = node.setdefault(k, {})
    node[keys[-1]] = value


def apply_overrides(cfg: dict, overrides: list[str] | None) -> dict:
    cfg = copy.deepcopy(cfg)
    for item in overrides or []:
        key, raw = item.split("=", 1)
        set_by_path(cfg, key, yaml.safe_load(raw))
    return cfg


# --------------------------------------------------------------------------- reproducibility
def set_all_seeds(seed: int) -> None:
    import torch
    from transformers import set_seed

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    set_seed(seed)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # bitsandbytes kernels are not fully deterministic; warn instead of failing.
    torch.use_deterministic_algorithms(True, warn_only=True)


def environment_info() -> dict:
    import torch
    import transformers
    import peft

    info = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "peft": peft.__version__,
        "cuda": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "gpu_total_mem_gib": round(torch.cuda.get_device_properties(0).total_memory / 2**30, 2)
        if torch.cuda.is_available() else None,
    }
    try:
        import bitsandbytes
        info["bitsandbytes"] = bitsandbytes.__version__
    except ImportError:
        info["bitsandbytes"] = None
    try:
        info["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        info["git_commit"] = None
    return info


# --------------------------------------------------------------------------- energy
class EnergyMeter:
    """GPU energy via NVML cumulative counter (Volta or newer). Returns None if unavailable."""

    def __init__(self):
        self.handle = None
        try:
            import pynvml
            pynvml.nvmlInit()
            self._nvml = pynvml
            self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            pynvml.nvmlDeviceGetTotalEnergyConsumption(self.handle)  # probe support
        except Exception:
            self.handle = None

    def read_mj(self):
        if self.handle is None:
            return None
        return self._nvml.nvmlDeviceGetTotalEnergyConsumption(self.handle)

    @staticmethod
    def wh(start_mj, end_mj):
        if start_mj is None or end_mj is None:
            return None
        return (end_mj - start_mj) / 3.6e6  # mJ -> Wh


# --------------------------------------------------------------------------- model
def build_model(cfg: dict):
    import torch
    from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig

    a = cfg["adaptation"]
    bits = int(a["bits"])
    compute_dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16

    quant_config = None
    if bits == 4:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=compute_dtype,
            llm_int8_skip_modules=["score", "classifier"],  # keep the classification head in full precision
        )
    elif bits == 8:
        quant_config = BitsAndBytesConfig(load_in_8bit=True, llm_int8_skip_modules=["score", "classifier"])
    elif bits != 16:
        raise NotImplementedError(f"{bits}-bit requires a GPTQ/AWQ backend (TODO).")

    tokenizer = AutoTokenizer.from_pretrained(cfg["model"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForSequenceClassification.from_pretrained(
        cfg["model"],
        num_labels=cfg["data"]["num_labels"],
        quantization_config=quant_config,
        torch_dtype=compute_dtype,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    model.config.pad_token_id = tokenizer.pad_token_id

    if quant_config is not None:
        model = prepare_model_for_kbit_training(
            model, use_gradient_checkpointing=cfg["training"].get("gradient_checkpointing", False)
        )

    lora = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=int(a["rank"]),
        lora_alpha=int(a["rank"]) * a.get("alpha_ratio", 2),
        lora_dropout=a.get("dropout", 0.05),
        target_modules=TARGET_MODULE_PRESETS[a["target_modules"]],
    )
    model = get_peft_model(model, lora)
    trainable, total = model.get_nb_trainable_parameters()
    return model, tokenizer, trainable, total


# --------------------------------------------------------------------------- data
def load_data(cfg: dict, tokenizer):
    from datasets import load_dataset

    d = cfg["data"]
    ds = load_dataset(d["dataset"], d.get("subset"))
    train = ds[d["train_split"]].shuffle(seed=cfg["seed"])
    evald = ds[d["eval_split"]]
    if d.get("max_train_samples"):
        train = train.select(range(min(d["max_train_samples"], len(train))))
    if d.get("max_eval_samples"):
        evald = evald.select(range(min(d["max_eval_samples"], len(evald))))

    def tok(batch):
        out = tokenizer(batch[d["text_field"]], truncation=True, max_length=d["max_length"])
        out["labels"] = batch[d["label_field"]]
        return out

    cols = train.column_names
    return train.map(tok, batched=True, remove_columns=cols), evald.map(tok, batched=True, remove_columns=cols), evald


# --------------------------------------------------------------------------- measurement
def measure_latency(model, tokenizer, raw_eval, cfg) -> tuple[float, float]:
    """Mean and std latency (ms) per single query, after warm-up."""
    import torch

    m = cfg["measurement"]
    texts = raw_eval[cfg["data"]["text_field"]][: m["latency_samples"] + m["latency_warmup"]]
    device = next(model.parameters()).device
    times = []
    model.eval()
    with torch.no_grad():
        for i, t in enumerate(texts):
            enc = tokenizer(t, return_tensors="pt", truncation=True, max_length=cfg["data"]["max_length"]).to(device)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            model(**enc)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            if i >= m["latency_warmup"]:
                times.append((time.perf_counter() - t0) * 1000)
    return float(np.mean(times)), float(np.std(times))


def peak_mem_gib() -> float | None:
    import torch
    return torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else None


def reset_peak_mem() -> None:
    import torch
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()


# --------------------------------------------------------------------------- main
def run(cfg: dict) -> dict:
    import torch
    from sklearn.metrics import accuracy_score, f1_score
    from transformers import DataCollatorWithPadding, Trainer, TrainingArguments

    run_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    set_all_seeds(cfg["seed"])
    energy = EnergyMeter()

    model, tokenizer, trainable, total = build_model(cfg)
    train_ds, eval_ds, raw_eval = load_data(cfg, tokenizer)
    t = cfg["training"]

    args = TrainingArguments(
        output_dir=str(ROOT / "checkpoints" / run_id),
        num_train_epochs=t["epochs"],
        per_device_train_batch_size=t["batch_size"],
        per_device_eval_batch_size=t["batch_size"],
        learning_rate=t["learning_rate"],
        gradient_checkpointing=t.get("gradient_checkpointing", False),
        bf16=torch.cuda.is_available() and torch.cuda.is_bf16_supported(),
        fp16=torch.cuda.is_available() and not torch.cuda.is_bf16_supported(),
        save_strategy="no",
        logging_steps=20,
        report_to="none",
        seed=cfg["seed"],
        data_seed=cfg["seed"],
    )

    def compute_metrics(p):
        preds = np.argmax(p.predictions, axis=-1)
        return {
            "accuracy": accuracy_score(p.label_ids, preds),
            "f1_macro": f1_score(p.label_ids, preds, average="macro"),
        }

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    # ---- training cost
    reset_peak_mem()
    e0, t0 = energy.read_mj(), time.perf_counter()
    trainer.train()
    train_time_s = time.perf_counter() - t0
    train_energy_wh = EnergyMeter.wh(e0, energy.read_mj())
    train_peak = peak_mem_gib()

    # ---- quality + inference cost
    reset_peak_mem()
    e1 = energy.read_mj()
    metrics = trainer.evaluate()
    eval_energy_wh = EnergyMeter.wh(e1, energy.read_mj())
    lat_mean, lat_std = measure_latency(model, tokenizer, raw_eval, cfg)
    infer_peak = peak_mem_gib()

    a = cfg["adaptation"]
    row = {
        "run_id": run_id,
        "experiment": cfg.get("experiment"),
        "model": cfg["model"],
        "dataset": f'{cfg["data"]["dataset"]}/{cfg["data"].get("subset")}',
        "bits": a["bits"],
        "rank": a["rank"],
        "target_modules": a["target_modules"],
        "seed": cfg["seed"],
        "trainable_params": trainable,
        "total_params": total,
        "accuracy": metrics.get("eval_accuracy"),
        "f1_macro": metrics.get("eval_f1_macro"),
        "train_peak_mem_gib": train_peak,
        "infer_peak_mem_gib": infer_peak,
        "train_time_s": train_time_s,
        "latency_ms_mean": lat_mean,
        "latency_ms_std": lat_std,
        "train_energy_wh": train_energy_wh,
        "eval_energy_wh": eval_energy_wh,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "runs.csv"
    new = not csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)

    log_dir = RESULTS_DIR / "runs"
    log_dir.mkdir(exist_ok=True)
    with open(log_dir / f"{run_id}.json", "w", encoding="utf-8") as f:
        json.dump({"config": cfg, "environment": environment_info(), "metrics": row}, f, indent=2, default=str)

    print(json.dumps(row, indent=2, default=str))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--set", nargs="*", default=[], help="Overrides, e.g. adaptation.rank=16 seed=22")
    args = ap.parse_args()
    run(apply_overrides(load_config(args.config), args.set))


if __name__ == "__main__":
    main()
