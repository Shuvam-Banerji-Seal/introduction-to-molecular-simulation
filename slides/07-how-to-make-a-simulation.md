---
marp: true
theme: default
paginate: true
header: "07 · How to Make a Simulation"
---

# 07 — How to make a simulation

### The 7-step workflow (live)

---

## The workflow

1. **Define the system** — atoms, box, PBC. (`packmol`, ASE, `gmx solvate`)
2. **Choose a potential** — LJ for learning; force field for production.
3. **Initial conditions** — lattice / solvate + Maxwell–Boltzmann velocities.
4. **Ensemble & integrator** — NVE (Verlet) → NVT (Langevin) → NPT (barostat).
5. **Equilibrate** — minimise → NVT → NPT; watch $T, P, E$, density.
6. **Produce** — fix seed, write trajectory (`.xyz` / `.dcd`), log observables.
7. **Analyse & validate** — RDF, MSD, energy traces; error bars; compare to experiment.

> Every example in `examples/` follows these steps — read any `run.py` top-to-bottom.

---

## Live demo — LJ fluid in 60 seconds

```bash
python examples/01-lennard-jones-fluid/run.py --steps 5000 --plot
# → trajectory.xyz  (view in OVITO/VMD)
# → energy.png      (check drift)
# → log: T*, P*, energy per particle
```

Try changing: `N`, `density`, `T*`, `dt` — see what breaks and why.

---

## Common beginner mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Wrong units | Explosion or frozen system | Use reduced units or check force-field units doc |
| Too large timestep | Energy drift, NaNs | Halve dt, re-test |
| No equilibration | Drift in T/P/density | Longer equilibration, monitor |
| Ignoring correlations | Tiny error bars that lie | Block averaging |
| Single seed | "It worked once" | Run 3 seeds, report spread |

*Full list: `docs/05-best-practices.md`.*

---

## Where to go next

- **MD engines:** LAMMPS (materials), GROMACS / OpenMM / NAMD (biomolecular), ASE (quick prototyping).
- **Analysis:** MDAnalysis, MDTraj, PyMBAR.
- **Enhanced sampling:** Umbrella, Metadynamics (PLUMED), Replica Exchange.
- **ML potentials:** MACE, NequIP, ANI — train on your chemistry.
- **Books:** Frenkel & Smit, Allen & Tildesley, Tuckerman.

---

## Take-home

> **Simulate with purpose, validate relentlessly, and always look at your trajectory.**

Repo: `github.com/Shuvam-Banerji-Seal/introduction-to-molecular-simulation`
Issues & PRs welcome — especially new examples!

### Thank you — questions?
