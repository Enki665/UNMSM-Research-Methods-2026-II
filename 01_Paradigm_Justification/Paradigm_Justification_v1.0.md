# Research Paradigm Justification Statement (v1.0)

PhD in Deep Tech — UNMSM · Session 1 · Edgar Aldair Quispe Huaman

## 1. Topic and context

Peru's underground mines depend on load-haul-dump loaders (scoops) and drilling jumbos operating in confined, harsh environments. When one of these machines fails unexpectedly, the consequence is not a metric: it is a stopped production face, a corrective repair that takes the machine out of service for a full day, and maintenance crews working under time pressure underground. Condition monitoring in these operations is still largely reactive or calendar-based. Telemetry is heterogeneous across equipment brands, and connectivity underground is intermittent: data reaches the surface only when a machine passes a communication point. Digital twins reported in industry assume dense sensing and continuous connectivity, conditions that mid-sized Peruvian underground operations do not meet.

## 2. Research question

How can a digital twin architecture based on cooperating AI agents be designed to monitor the condition of underground extraction equipment under intermittent connectivity and heterogeneous telemetry, and how can it be evaluated, in terms of its fidelity as a model and its utility for maintenance decisions compared with reactive and calendar-based maintenance, so that its design principles transfer across equipment types?

## 3. Paradigm and justification

I adopt **Design Science** (Hevner et al., 2004) as the governing paradigm: the contribution is an artifact, a multi-agent digital twin architecture, together with transferable design principles. In Gregor & Hevner's (2013) terms it is an **exaptation**: digital twins and agent-based monitoring are known solutions, applied here to a new problem context defined by underground operation, intermittent connectivity and heterogeneous fleets. I do not adopt **positivism** as the governing paradigm; I borrow its controlled, replicated experiments as the rigor cycle that evaluates the artifact, so positivism produces my evidence, not my contribution. I reject **interpretivism** because the core problem is the physical condition of machines and the timing of maintenance decisions, not the meaning operators give to the technology. I reject **mixed methods** because a qualitative strand would not be integrated into the central claim; it would be appended to the artifact evaluation rather than producing a finding neither strand could reach alone.

## 4. Implications

- **(a) Data:** simulated fleet telemetry with controlled degradation and fault injection, public run-to-failure benchmarks for validation, and, in a later phase, real telemetry from a partner mining operation.
- **(b) Methods:** build–evaluate design cycles: model validity first (fidelity of the twin's condition estimates against known ground truth), then decision utility (paired comparison of agent-assisted maintenance against reactive and calendar-based policies under common random numbers).
- **(c) Contribution:** the multi-agent digital twin architecture, an open simulation testbed and transferable design principles for underground equipment monitoring.
- **(d) Target venues:** IEEE *Transactions on Industrial Informatics*, *Reliability Engineering & System Safety* and *International Journal of Mining Science and Technology*; DESRIST for the design principles.

## 5. One doubt or tension

My strongest tension is external validity. Until a mining company confirms access to real telemetry, the artifact is evaluated in simulation and on public benchmarks from other machinery, so the twin may learn the assumptions of my own simulator. I address this by validating the simulator against public run-to-failure data and by planning a field validation phase whose data access I am negotiating in parallel.

## References

- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research for maximum impact. *MIS Quarterly, 37*(2), 337–355.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75–105.
