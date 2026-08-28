---
marp: true
theme: default
paginate: true
header: "01 · What is Molecular Simulation?"
---

# 01 — What is molecular simulation?

---

## The core idea

We **model a system of atoms/molecules**, propagate it with physics, and **measure macroscopic properties** as ensemble/time averages.

```
Real system  →  Model (Hamiltonian)  →  Sampling (MD/MC)  →  Observables
  (lab)          (potentials)           (trajectory)        (pressure, RDF, D, ΔG …)
```

> Simulation is a **computational microscope** — and a **computational experiment**.

---

## Why not just do the experiment?

| Simulation gives you | Experiment struggles with |
|---|---|
| Atom-by-atom mechanism | Buried intermediates, rare events |
| Exact control of conditions | Extreme T / P, toxic systems |
| Free energies & entropy | Direct free-energy measurement |
| Cheap "what if?" | Synthesis cost, safety |

But: **a simulation is only as good as its model** — validation is non-negotiable.

---

## The statistical mechanics bridge

- Microscopic states → macroscopic observables via **ensembles**.
- Ergodic hypothesis: **time average = ensemble average** (for ergodic systems).
- Boltzmann weight: $p \propto e^{-\beta U}$ — low-energy states dominate.
- Partition function $Z$ → free energy $F = -k_BT \ln Z$ → everything.

*More in `docs/01-statistical-mechanics-bridge.md`.*

---

## MD vs MC — the two workhorses

|  | **Molecular Dynamics (MD)** | **Monte Carlo (MC)** |
|---|---|---|
| Moves | Deterministic (Newton) | Stochastic (random + accept/reject) |
| Time | Real dynamics, kinetics | No physical time (but great sampling) |
| Best for | Transport, spectra, non-equilibrium | Phase equilibria, free energy |
| Integrator / Rule | Verlet, Langevin, … | Metropolis, … |

Many real workflows use **both**.

---

## What you will be able to do after this talk

1. Sketch the 7-step simulation workflow from memory.
2. Write a minimal LJ fluid MD in <100 lines of Python.
3. Choose an ensemble and explain *why*.
4. Spot the three most common beginner mistakes (units, equilibration, correlation).

*Next: what actually moves the atoms — potentials & force fields.*
