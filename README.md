# Introduction to Molecular Simulation

> A beginner-friendly talk + hands-on companion repo: **what molecular simulation is, why it works, and how to run one yourself.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](environment.yml)
[![Slides: Marp](https://img.shields.io/badge/slides-Marp-red)](slides/)

---

## Talk Abstract

Molecular simulation bridges the microscopic world of atoms and molecules to the macroscopic properties we measure in the lab — pressure, solubility, diffusion, binding affinity. This talk introduces the core ideas with minimal prerequisites:

1. **Why simulate?** The statistical mechanics link (micro → macro via ensembles).
2. **What moves atoms?** Potentials & force fields — from Lennard-Jones to modern ML potentials.
3. **How do we move them?** Molecular Dynamics (integrators, thermostats, barostats) vs Monte Carlo (importance sampling).
4. **What ensemble are we in?** NVE / NVT / NPT — choosing and controlling thermodynamic conditions.
5. **What do we measure?** Structure (RDF), dynamics (MSD, VACF), thermodynamics (free energy), and how to avoid fooling yourself.
6. **How to make a simulation** — a live, reproducible workflow from zero to trajectory.

No prior simulation experience assumed. Bring curiosity; leave with a running simulation.

---

## Repository Structure

```
.
├── slides/                  # Talk deck — Marp-flavored Markdown (exports to PDF/PPTX/HTML)
│   ├── 00-title-and-outline.md
│   ├── 01-what-is-molecular-simulation.md
│   ├── 02-potentials-and-force-fields.md
│   ├── 03-molecular-dynamics.md
│   ├── 04-monte-carlo.md
│   ├── 05-ensembles-and-thermodynamics.md
│   ├── 06-analysis-and-visualization.md
│   └── 07-how-to-make-a-simulation.md
├── docs/                    # Concept notes (deeper than slides, still introductory)
│   ├── 01-statistical-mechanics-bridge.md
│   ├── 02-potentials.md
│   ├── 03-integrators.md
│   ├── 04-ensembles.md
│   ├── 05-best-practices.md
│   └── glossary.md
├── examples/                # Runnable examples — numbered, self-contained
│   ├── 01-lennard-jones-fluid/   # NVE MD in reduced LJ units (pure Python)
│   ├── 02-langevin-dynamics/     # Thermostat & temperature control
│   ├── 03-monte-carlo-lj/        # Metropolis MC in the NVT ensemble
│   ├── 04-water-box/             # Solvated water box (OpenMM/ASE, optional deps)
│   └── 05-analysis/              # RDF, MSD, energy & temperature traces
├── assets/                  # Figures & diagrams
├── environment.yml          # Conda environment
├── requirements.txt         # pip requirements
├── CITATION.cff             # Citation metadata
├── LICENSE                  # MIT
└── plans/                   # Build log for this repo (rigor-infinity work journal)
```

---

## Quick Start

### Option A — Conda (recommended)

```bash
conda env create -f environment.yml
conda activate intro-molsim
```

### Option B — pip + venv

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Examples

> **Current status:** Repo structure is ready — runnable scripts for `examples/01`–`05` will be added next. Each example folder already has a placeholder `README.md` describing the planned content.

```bash
# Once scripts land (coming next):
# python examples/01-lennard-jones-fluid/run.py
# python examples/02-langevin-dynamics/run.py
```

> Planned stack: Examples `01`–`03` will need only **NumPy + Matplotlib**.  
> Example `04` (water box) will optionally use **OpenMM** or **ASE**.  
> Example `05` will use **MDAnalysis** when available, with a pure-NumPy fallback.

---

## Prerequisites

| You need | Why | Minimum |
|---|---|---|
| Python 3.9+ | Run examples | `python --version` |
| NumPy, Matplotlib | Core numerics & plots | in `requirements.txt` |
| (Optional) OpenMM / ASE | Realistic water/biomolecular systems | `conda install -c conda-forge openmm ase` |
| (Optional) MDAnalysis, nglview | Analysis & visualization | `pip install MDAnalysis` |
| (Optional) Marp CLI | Export slides to PDF | `npm i -g @marp-team/marp-cli` |

No compiled MD engine (LAMMPS/GROMACS) required for the intro examples.

---

## How to Make a Simulation — The 7-Step Workflow

> This is the backbone of the talk. Every example follows it.

1. **Define the system** — atoms, box, boundary conditions.
2. **Choose a potential** — Lennard-Jones, harmonic bonds, Coulomb, or a force field (AMBER, CHARMM, OPLS, …).
3. **Set initial conditions** — positions (lattice / solvate) + velocities (Maxwell–Boltzmann).
4. **Pick an ensemble & integrator** — NVE (Verlet), NVT (Langevin/Nosé-Hoover), NPT (barostat).
5. **Equilibrate** — relax, monitor temperature/pressure/energy.
6. **Produce & sample** — collect trajectory, control random seeds, write outputs.
7. **Analyse & validate** — RDF, MSD, energy conservation, convergence, error bars.

`docs/05-best-practices.md` expands each step with common pitfalls.

---

## Slides

Slides are written in **Marp Markdown** — they render directly on GitHub and export to PDF/PPTX/HTML:

```bash
# Export all decks to PDF (requires Marp CLI)
marp slides/00-title-and-outline.md --pdf -o slides.pdf
# Or export the whole folder:
marp slides/ --pdf --output pdf/
```

You can also present directly from VS Code with the Marp extension.

---

## Learning Path

| Order | Read / Do | Time |
|---|---|---|
| 1 | Slides `00` → `02` + `docs/01` | 30 min |
| 2 | Run `examples/01` + read its README | 20 min |
| 3 | Slides `03` → `05` + `docs/03`, `docs/04` | 40 min |
| 4 | Run `examples/02` & `03`, compare NVE vs NVT vs MC | 30 min |
| 5 | `examples/04` + `05` (analysis) | 30 min |
| 6 | `docs/05-best-practices.md` before your first "real" system | 15 min |

---

## References

- Frenkel & Smit — *Understanding Molecular Simulation* (3rd ed.)
- Allen & Tildesley — *Computer Simulation of Liquids* (2nd ed.)
- Tuckerman — *Statistical Mechanics: Theory and Molecular Simulation*
- Leach — *Molecular Modelling: Principles and Applications*

See `docs/` for inline citations and `CITATION.cff` to cite this repo.

---

## Contributing & Reuse

PRs and issues welcome — especially corrections, clearer figures, or extra examples (e.g. free-energy, enhanced sampling).  
This is teaching material: reuse freely under MIT, attribution appreciated.

## License

MIT — see [LICENSE](LICENSE).

---

*Built as a companion to a live talk. If you attended, the examples are the take-home lab. If you didn't, they still work — start at `examples/01-lennard-jones-fluid/README.md`.*
