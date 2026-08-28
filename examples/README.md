# Examples

Runnable, self-contained examples that follow the **7-step workflow**. Each folder has its own `README.md` + `run.py`.

| # | Example | Ensemble | Needs | Time |
|---|---|---|---|---|
| 01 | **Lennard-Jones fluid (NVE)** | NVE | NumPy, Matplotlib | <5 s |
| 02 | **Langevin dynamics (NVT)** | NVT | NumPy, Matplotlib | <5 s |
| 03 | **Monte Carlo LJ (NVT)** | NVT (MC) | NumPy, Matplotlib | <5 s |
| 04 | **Water box** | NPT (optional) | OpenMM *or* ASE (optional) | <30 s |
| 05 | **Analysis — RDF, MSD, energy** | — | NumPy; MDAnalysis optional | <5 s |

## Quick run

```bash
# From repo root, after conda/pip setup:
python examples/01-lennard-jones-fluid/run.py
python examples/02-langevin-dynamics/run.py
python examples/03-monte-carlo-lj/run.py
python examples/04-water-box/run.py        # prints guidance if OpenMM/ASE missing
python examples/05-analysis/run.py         # analyses trajectories from 01-03 if present
```

## Notes

- Examples `01`–`03` use **reduced Lennard-Jones units** ($\sigma=\varepsilon=m=k_B=1$) so no unit confusion.
- Each `run.py` accepts `--help` for options (steps, seed, plot, etc.).
- Outputs (`trajectory.xyz`, `*.png`, `*.npy`) are `.gitignore`'d — generate locally.
- All examples set a **fixed random seed** by default for reproducibility; change with `--seed`.

## Learning order

`01` → `02` → `03` → `05` → `04` (if you have OpenMM/ASE).
