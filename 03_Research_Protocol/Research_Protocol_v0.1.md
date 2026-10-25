# Research Protocol Outline (v0.1)

PhD in Deep Tech · UNMSM · Session 3 · Edgar Aldair Quispe Huaman

## 01 · Title

A multi-agent digital twin architecture for condition monitoring of underground extraction equipment under intermittent connectivity: load-haul-dump loaders in Peruvian underground mining.

*Arquitectura de gemelo digital basada en agentes de inteligencia artificial para el monitoreo de la condición de equipos de extracción en minería subterránea peruana.*

## 02 · Abstract

Underground mines in Peru depend on load-haul-dump loaders (scoops) and drilling jumbos whose unplanned failures stop production faces and force day-long corrective repairs. Condition monitoring in these operations remains largely reactive or calendar-based, telemetry is heterogeneous across fleets, and connectivity underground is intermittent. Digital twins reported in the literature typically assume dense sensing and continuous data transmission. Grounded in Design Science Research (DSR), this doctoral project designs, builds and evaluates a digital twin architecture in which cooperating AI agents perceive equipment condition from partial telemetry, diagnose degradation and plan maintenance under crew-capacity constraints, keeping a human in the loop for every intervention. Evaluation proceeds in three stages: model validity of the twin's condition estimates against ground truth in a calibrated simulation testbed and on public run-to-failure benchmarks; decision utility, comparing agent-assisted maintenance with reactive and calendar-based policies in paired replications under common random numbers; and transferability, re-validating the design on a second equipment type and, when access is confirmed, on real fleet telemetry. The expected contribution is an exaptation-type artifact (Gregor & Hevner, 2013), an open simulation testbed and transferable design principles for monitoring underground equipment.

## 03 · Introduction & Problem Statement ("So What?" Test)

- **The empirical gap:** digital twins for industrial assets are well established in manufacturing (Kritzinger et al., 2018; Tao et al., 2019), and condition-based maintenance has a mature diagnostic and prognostic basis (Jardine et al., 2006). Underground mining equipment, however, operates under intermittent connectivity, heterogeneous brands and partial sensing, conditions under which the assumption of a continuously synchronized twin does not hold.
- **Why care ("So What?"):** every unplanned failure of a loader underground means a stopped production face, a corrective repair of about a day and maintenance work under pressure in a hazardous environment. A twin that works with the telemetry mines already have, and that recommends rather than executes interventions, offers a deployable path to fewer unplanned stops without new sensor investment.

## 04 · Literature Review Axes

1. **Digital twins:** concept and classification (Grieves & Vickers, 2017; Kritzinger et al., 2018; Tao et al., 2019).
2. **Condition monitoring and prognostics:** diagnostics, prognostics and condition-based maintenance (Jardine et al., 2006); run-to-failure benchmarks (Saxena et al., 2008).
3. **Intelligent agents and multi-agent systems:** autonomy, cooperation and decision support (Wooldridge & Jennings, 1995).
4. **Mining equipment and underground operations:** load-haul-dump loaders, drilling jumbos, connectivity and safety constraints.
5. **Design science evaluation:** FEDS framework (Venable et al., 2016) and DSR methodology (Peffers et al., 2007).

The systematic review that consolidates these axes is in [04_Literature_Review_PRISMA](../04_Literature_Review_PRISMA/).

## 05 · Research Questions, Objectives & Hypotheses

**General question:** To what extent does a multi-agent digital twin architecture improve the condition monitoring and maintenance of underground extraction equipment under intermittent connectivity, compared with reactive and calendar-based maintenance?

**General objective:** Design, build and evaluate a multi-agent digital twin architecture for condition monitoring of underground extraction equipment.

| | Specific question | Specific objective | Hypothesis |
|---|---|---|---|
| SO1 | How faithfully can the twin estimate equipment condition from partial, intermittently transmitted telemetry? | Validate the fidelity of the twin's condition estimates against ground truth. | HE1: the twin detects degradation before functional failure in a significantly larger share of cases than fixed-threshold alarms. |
| SO2 | Does agent-assisted maintenance improve availability and reduce unplanned failures and cost? | Evaluate the decision utility of the twin against reactive and calendar-based policies. | HE2: agent-assisted maintenance significantly reduces unplanned failures and increases availability compared with both baselines, at a maintenance cost not greater than calendar-based maintenance. |
| SO3 | How does the twin's utility change as connectivity degrades? | Characterize the sensitivity of the twin to the probability of data transmission. | HE3: the twin's advantage over calendar-based maintenance remains significant down to a minimum connectivity level that can be identified empirically. |
| SO4 | Do the design principles transfer across equipment types and data sources? | Re-validate the architecture on a second equipment type and on real or public run-to-failure data. | HE4: the improvement remains significant when the architecture is applied to a second equipment type. |

**Baselines:** reactive maintenance (repair on failure) and calendar-based preventive maintenance at a fixed interval.

## 06 · Methodology

- **Paradigm:** Design Science (Hevner et al., 2004), with positivist experimentation as the rigor cycle.
- **Process:** DSR methodology of Peffers et al. (2007); evaluation strategy following FEDS (Venable et al., 2016): formative, artificial evaluation in simulation first, then summative, naturalistic evaluation with real telemetry.
- **Artifact:** three cooperating agents. A perception agent fuses intermittent telemetry into a condition state; a diagnosis agent scores deviations from healthy behavior (Mahalanobis distance with exponential smoothing in the pilot); a planning agent prioritizes interventions under crew-capacity constraints. Every intervention is recommended to a human planner.
- **Testbed:** a fleet simulator with stochastic degradation, duty cycles, sensor noise and intermittent connectivity, calibrated against public run-to-failure data.
- **Unit of analysis:** one simulation replication of the fleet under one policy. Replications use common random numbers, so policies are compared on identical degradation, duty and connectivity trajectories.
- **Design:** 30 paired replications per scenario; factors in later stages: connectivity probability, fleet heterogeneity and crew capacity.
- **Statistical analysis:** Wilcoxon signed-rank tests on paired replications, rank-biserial effect sizes, bootstrap 95% confidence intervals and Holm correction for multiple comparisons.
- **Reproducibility:** fixed seeds, configuration and environment logged per run, public code in [05_Reproducible_ML_Pipeline](../05_Reproducible_ML_Pipeline/).

**Pilot result (simulation, 30 paired replications, 10 loaders, 90 days):** the twin eliminated unplanned failures (0.00 vs. 25.83 reactive and 0.73 calendar-based) and raised availability over reactive maintenance (0.987 vs. 0.972), but intervened more often than the calendar-based policy, at a higher maintenance cost (115.3 vs. 85.9 relative units) and slightly lower availability (0.987 vs. 0.990). The pilot therefore supports the reduction of unplanned failures and identifies the calibration of the alarm threshold as the next design iteration.

## 07 · Ethics, Governance & Data Protection

- **Scientific integrity:** compliance with CONCYTEC's National Code of Scientific Integrity; hypotheses and analysis plan specified before each evaluation stage; all replications reported, including unfavorable results such as the pilot's higher maintenance cost.
- **Data protection:** simulated and public data contain no personal data. Real fleet telemetry may include operator identifiers; these are pseudonymized before analysis and handled under Law N° 29733 and its Regulation, with a data-sharing agreement signed with the partner company.
- **Occupational safety:** the twin operates in recommendation mode with a human planner in the loop, consistent with the occupational health and safety regulation for mining (D.S. N° 024-2016-EM and its amendments).
- **AI regulation:** alignment with Law N° 31814, which promotes the use of artificial intelligence in Peru, and its Regulation.
- **AI-use declaration:** generative AI was used for structuring, preliminary drafting and code scaffolding; methodological decisions are the author's own.

## 08 · Expected Results

1. A validated multi-agent digital twin architecture for underground extraction equipment, released as open-source software.
2. An open simulation testbed for evaluating maintenance policies under intermittent connectivity.
3. Evidence on fidelity and decision utility, and transferable design principles published in target venues (IEEE TII, Reliability Engineering & System Safety, DESRIST).

## 09 · Timeline & Budget (36 months)

- **Months 1–6:** protocol refinement, systematic review, ethics committee approval and negotiation of a data-sharing agreement with a mining company.
- **Months 7–16:** simulator calibration with public run-to-failure data, agent design and model validity evaluation (SO1).
- **Months 17–26:** decision utility and connectivity sensitivity experiments (SO2, SO3); first publication.
- **Months 27–36:** transfer to a second equipment type and naturalistic validation with real telemetry (SO4), thesis writing and defense.
- **Budget:** cloud and local compute, edge hardware for a field prototype, article processing charges and conference participation, editing services and a 10% contingency, financed through UNMSM competitive funds and national science and technology calls.

## 10 · Core Bibliography

- Grieves, M., & Vickers, J. (2017). Digital twin: Mitigating unpredictable, undesirable emergent behavior in complex systems. In F.-J. Kahlen, S. Flumerfelt, & A. Alves (Eds.), *Transdisciplinary perspectives on complex systems* (pp. 85–113). Springer.
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105.
- Jardine, A. K. S., Lin, D., & Banjevic, D. (2006). A review on machinery diagnostics and prognostics implementing condition-based maintenance. *Mechanical Systems and Signal Processing, 20*(7), 1483–1510.
- Kritzinger, W., Karner, M., Traar, G., Henjes, J., & Sihn, W. (2018). Digital twin in manufacturing: A categorical literature review and classification. *IFAC-PapersOnLine, 51*(11), 1016–1022.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77.
- Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. *International Conference on Prognostics and Health Management*.
- Tao, F., Zhang, H., Liu, A., & Nee, A. Y. C. (2019). Digital twin in industry: State-of-the-art. *IEEE Transactions on Industrial Informatics, 15*(4), 2405–2415.
- Venable, J., Pries-Heje, J., & Baskerville, R. (2016). FEDS: A framework for evaluation in design science research. *European Journal of Information Systems, 25*(1), 77–89.
- Wooldridge, M., & Jennings, N. R. (1995). Intelligent agents: Theory and practice. *The Knowledge Engineering Review, 10*(2), 115–152.
