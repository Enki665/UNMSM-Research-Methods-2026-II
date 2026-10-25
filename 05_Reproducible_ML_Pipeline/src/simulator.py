from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Exogenous:
    increments: np.ndarray
    duty: np.ndarray
    noise: np.ndarray
    connected: np.ndarray


def generate_exogenous(cfg: dict, seed: int) -> Exogenous:
    rng = np.random.default_rng(seed)
    f, d, s = cfg["fleet"], cfg["degradation"], cfg["sensors"]
    n, T = f["n_units"], f["horizon_hours"]
    k = d["gamma_shape"]
    unit_rate = rng.lognormal(0.0, d["unit_heterogeneity_sigma"], size=n)
    theta = (1.0 / d["mean_life_hours"]) / k
    increments = rng.gamma(k, theta, size=(T, n)) * unit_rate
    duty = np.clip(rng.normal(f["mean_duty"], 0.15, size=(T, n)), 0.1, 1.0)
    noise = rng.normal(0.0, 1.0, size=(T, n, len(s["names"]))) * np.asarray(s["noise_sd"])
    connected = rng.random((T, n)) < cfg["connectivity"]["p_connected"]
    return Exogenous(increments, duty, noise, connected)


def sensor_readings(cfg: dict, health: np.ndarray, duty: np.ndarray, noise: np.ndarray) -> np.ndarray:
    s = cfg["sensors"]
    wear = (1.0 - np.clip(health, 0.0, 1.0)) ** 2
    return (
        np.asarray(s["base"])
        + duty[:, None] * np.asarray(s["duty_effect"])
        + wear[:, None] * np.asarray(s["degradation_effect"])
        + noise
    )


class TwinAgents:
    def __init__(self, cfg: dict):
        a = cfg["policies"]["twin_agent"]
        self.alpha = a["ewma_alpha"]
        self.quantile = a["alarm_quantile"]
        self.k = a["consecutive_alarms"]
        self.mean = None
        self.inv_cov = None
        self.threshold = None
        self.score = None
        self.streak = None

    def fit_baseline(self, X: np.ndarray, n_units: int) -> None:
        self.mean = X.mean(axis=0)
        self.inv_cov = np.linalg.pinv(np.cov(X, rowvar=False))
        self.threshold = np.quantile(self._mahalanobis(X), self.quantile)
        self.score = np.zeros(n_units)
        self.streak = np.zeros(n_units, dtype=int)

    def _mahalanobis(self, X: np.ndarray) -> np.ndarray:
        diff = X - self.mean
        return np.sqrt(np.einsum("ij,jk,ik->i", diff, self.inv_cov, diff))

    def observe(self, units: np.ndarray, X: np.ndarray) -> None:
        if len(units) == 0:
            return
        d = self._mahalanobis(X)
        self.score[units] = self.alpha * d + (1 - self.alpha) * self.score[units]
        above = self.score[units] > self.threshold
        self.streak[units] = np.where(above, self.streak[units] + 1, 0)

    def candidates(self, eligible: np.ndarray) -> np.ndarray:
        idx = np.where(eligible & (self.streak >= self.k))[0]
        return idx[np.argsort(-self.score[idx])]

    def reset(self, unit: int) -> None:
        self.score[unit] = 0.0
        self.streak[unit] = 0


def simulate(cfg: dict, exo: Exogenous, policy: str) -> dict:
    f, m = cfg["fleet"], cfg["maintenance"]
    n, T, warm = f["n_units"], f["horizon_hours"], f["warmup_hours"]
    health = np.ones(n)
    downtime = np.zeros(n, dtype=int)
    in_preventive = np.zeros(n, dtype=bool)
    age = np.zeros(n)
    operating_hours = 0
    failures = preventive = unnecessary = 0
    agents = TwinAgents(cfg) if policy == "twin_agent" else None
    baseline = []

    for t in range(T):
        finishing = downtime == 1
        health[finishing] = 1.0
        age[finishing] = 0.0
        in_preventive[finishing] = False
        downtime[downtime > 0] -= 1

        op = downtime == 0
        health[op] -= exo.increments[t, op] * exo.duty[t, op] / f["mean_duty"]
        age[op] += 1
        failed = op & (health <= 0)
        failures += int(failed.sum())
        downtime[failed] = m["corrective_hours"]
        if agents is not None:
            for u in np.where(failed)[0]:
                agents.reset(u)
        op = downtime == 0
        operating_hours += int(op.sum())

        X = sensor_readings(cfg, health, exo.duty[t], exo.noise[t])

        if policy == "twin_agent":
            if t < warm:
                baseline.append(X[op])
                if t == warm - 1:
                    agents.fit_baseline(np.vstack(baseline), n)
                continue
            seen = np.where(op & exo.connected[t])[0]
            agents.observe(seen, X[seen])
            free = m["crew_capacity"] - int(in_preventive.sum())
            chosen = agents.candidates(op)[: max(free, 0)]
        elif policy == "preventive":
            free = m["crew_capacity"] - int(in_preventive.sum())
            due = np.where(op & (age >= cfg["policies"]["preventive_interval_hours"]))[0]
            chosen = due[np.argsort(-age[due])][: max(free, 0)]
        else:
            chosen = np.array([], dtype=int)

        for u in chosen:
            preventive += 1
            unnecessary += int(health[u] > m["unnecessary_health_threshold"])
            downtime[u] = m["preventive_hours"]
            in_preventive[u] = True
            if agents is not None:
                agents.reset(u)

    total = n * T
    return {
        "availability": operating_hours / total,
        "unplanned_failures": failures,
        "preventive_interventions": preventive,
        "unnecessary_interventions": unnecessary,
        "maintenance_cost": failures * m["corrective_cost"] + preventive * m["preventive_cost"],
        "unplanned_downtime_hours": failures * m["corrective_hours"],
    }
