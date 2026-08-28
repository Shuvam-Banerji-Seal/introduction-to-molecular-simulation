# Glossary

| Term | Meaning |
|---|---|
| **PES** | Potential Energy Surface — $U(\mathbf{r}^N)$ |
| **Force field** | Parameterized functional form for $U$ (bonds, angles, LJ, Coulomb, …) |
| **PBC** | Periodic Boundary Conditions — infinite tiling via image cells |
| **NVE / NVT / NPT** | Ensembles (microcanonical / canonical / isothermal-isobaric) |
| **Integrator** | Algorithm advancing $\mathbf{r},\mathbf{v}$ in time (e.g. Velocity Verlet) |
| **Thermostat** | Coupling to a heat bath to control T (Langevin, Nosé-Hoover, …) |
| **Barostat** | Coupling to a pressure bath to control P |
| **RDF / g(r)** | Radial Distribution Function — pair structure vs distance |
| **MSD** | Mean Squared Displacement — dynamics / diffusion |
| **VACF** | Velocity Autocorrelation Function |
| **MC** | Monte Carlo — stochastic sampling via accept/reject |
| **Metropolis** | MC acceptance rule $P_{\rm acc}=\min(1,e^{-\beta\Delta U})$ |
| **Ergodic** | Time average = ensemble average (if sampling is complete) |
| **Reduced units** | LJ units where $\sigma=\varepsilon=m=k_B=1$ |
| **Cutoff** | Distance beyond which interactions are ignored (with corrections) |
| **PME / Ewald** | Long-range electrostatics methods |
| **Free energy** | $F=-k_BT\ln Z$ — determines stability & spontaneity |
| **Enhanced sampling** | Umbrella, metadynamics, replica exchange — for rare events |
