# Research Method-Fit Matrix (v1.0)

PhD in Deep Tech — UNMSM · Session 2 · Edgar Aldair Quispe Huaman

## 1. Refined research question

Can a multi-agent digital twin architecture monitor the condition of underground load-haul-dump loaders under intermittent connectivity with sufficient fidelity, and does it improve maintenance decisions (availability, unplanned failures and maintenance cost) compared with reactive and calendar-based maintenance?

## 2. Candidate methods (all viable)

- **A. Design Science.** Build the multi-agent digital twin and evaluate it in design cycles: fidelity against ground truth, then decision utility in replicated, paired experiments.
- **B. Simulation study.** Model the fleet and compare maintenance policies through discrete-event simulation, without building a deployable twin.
- **C. Case study.** Study condition monitoring and maintenance decisions in depth at one underground mine through interviews, observation and maintenance records.

## 3. Matrix (scores 1–5, gate applied before totals)

| Criterion | Weight | A. Design Science | B. Simulation | C. Case study | Justification |
|---|---|---|---|---|---|
| E · Epistemological fit | 30 | 5 | 3 | **2** | My paradigm is DSR: knowledge through a built, evaluated artifact. B answers what-if questions but produces no artifact. C describes a site without building a solution. |
| D · Data availability | 15 | 4 | 5 | 2 | A and B can start with simulated and public data. C depends entirely on company access, which is not yet confirmed. |
| F · Feasibility | 15 | 3 | 5 | 3 | A is the most demanding: architecture, simulator and agents. B is cheapest. C requires sustained presence underground. |
| C · Contribution type | 25 | 5 | 3 | 2 | The goal is a reusable twin architecture with design principles. B yields policy comparisons; C yields contextual understanding. |
| V · Venue fit | 15 | 4 | 4 | 3 | Industrial informatics and mining journals publish both artifacts and simulation studies; single-site case studies are weaker there. |
| **Gate (E ≤ 2 eliminates)** | | Survives | Survives | **ELIMINATED** | |
| **Weighted score (/5)** | 100 | **4.40** | 3.75 | — | |

## 4. Weights: highest and lowest

- **Highest, E (30):** a method that cannot express knowledge through making would contradict my Session 1 paradigm, and no feasibility or venue advantage can compensate for that.
- **Lowest tier, D, F and V (15 each):** data and feasibility are real risks in mining, but they are constraints I can manage through simulation and public data, whereas a wrong contribution type cannot be repaired later.

## 5. Winning method: Design Science

I choose Design Science because my contribution is a **multi-agent digital twin architecture with demonstrated fidelity and decision utility**, plus transferable design principles. Simulation is used inside the design cycle as the evaluation testbed, not as the contribution. I reject the **simulation study** because comparing maintenance policies in a model does not produce an artifact that can be deployed underground. I reject the **case study** because it would describe one mine's maintenance practice without building a solution, and because its data access is not yet confirmed.

*(Gregor & Hevner, 2013: the contribution type is **exaptation**: known solutions, digital twins and agent-based monitoring, applied to the new context of underground equipment under intermittent connectivity.)*

## 6. Exit commitment

"I will use Design Science with replicated experimental evaluation because my contribution is a digital twin artifact whose fidelity and decision utility must be demonstrated, and I reject the case study because, specifically, it would describe maintenance practice at one mine without producing a transferable artifact."

**Open tension:** data availability (D = 4 for the winning method) depends on simulation and public data until real telemetry is confirmed.
