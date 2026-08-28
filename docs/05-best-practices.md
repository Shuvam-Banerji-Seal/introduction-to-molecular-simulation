# Best Practices — How Not to Fool Yourself

## The 7-step workflow revisited

1. **Define the system** — atoms, box, PBC. Use `packmol` / ASE / `gmx solvate`.
2. **Choose a potential** — force field validated for your chemistry.
3. **Initial conditions** — lattice/solvate + Maxwell–Boltzmann velocities (set seed!).
4. **Ensemble & integrator** — pick dt, thermostat, barostat.
5. **Equilibrate** — minimise → NVT → NPT; monitor T, P, E.
6. **Produce** — fixed seed, write trajectory + logs.
7. **Analyse** — RDF, MSD, error bars; compare to experiment.

## Common pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Wrong units | Explosion / frozen system | Check force-field docs; use reduced units for toys |
| Too large dt | Energy drift, NaNs, crash | Halve dt |
| No equilibration | Drifting T/P/density | Extend equilibration, discard initial segment |
| Ignoring correlations | Unrealistically small error bars | Block averaging / bootstrap |
| Single seed | "Worked once" | Run ≥3 seeds, report spread |
| Cutoff artefacts | Wrong pressure/structure | Increase $r_c$, add tail corrections, PME for Coulomb |

## Reproducibility

- Fix random seeds and **report them**.
- Version-pin your MD engine and force field.
- Store inputs (topology, config) alongside outputs.
- Use a workflow manager (Snakemake, AiiDA) for production.

## Validation ladder

1. **Conservation** — NVE energy drift < 0.1% over production.
2. **Stability** — $\langle T\rangle$, $\langle P\rangle$ at target.
3. **Convergence** — averages plateau with more sampling.
4. **Reproducibility** — independent runs agree within error.
5. **Experiment** — density, RDF, diffusion within expected range.

## Performance notes

- Start small (N=100–500) to iterate fast, then scale.
- Profile before optimising; neighbour lists dominate cost.
- GPU helps for large N; for N<10k, CPU is often fine.
