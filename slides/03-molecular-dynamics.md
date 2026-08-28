---
marp: true
theme: default
paginate: true
header: "03 · Molecular Dynamics"
---

# 03 — Molecular Dynamics

---

## Newton's equations, numerically

$$m_i \ddot{\mathbf{r}}_i = \mathbf{F}_i = -\nabla_i U$$

We discretize time: $\mathbf{r}(t+\Delta t)$ from $\mathbf{r}(t), \mathbf{v}(t), \mathbf{F}(t)$.

Requirements for an integrator: **time-reversible, symplectic, stable, cheap**.

---

## Velocity Verlet — the default

```
r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt^2
compute forces → a(t+dt)
v(t+dt) = v(t) + 0.5*(a(t)+a(t+dt))*dt
```

- Symplectic → excellent energy conservation in NVE.
- Needs small enough $\Delta t$ (~1 fs in real units; ~0.005 in LJ reduced units).
- Demo: `examples/01-lennard-jones-fluid/run.py` checks energy drift.

---

## Temperature control — thermostats

MD is naturally **NVE**. To get **NVT**, couple to a heat bath:

| Thermostat | Idea | Notes |
|---|---|---|
| **Langevin** | Friction + random kicks | Simple, robust — demo in `02-langevin-dynamics` |
| Nosé-Hoover | Extended variable | Deterministic, needs tuning |
| Velocity rescale | Simple rescaling | Stochastic variant (Bussi) preferred |

> Validate: velocity distribution should be Maxwell–Boltzmann.

---

## Pressure control — barostats

For **NPT**: Berendsen (quick, not correct ensemble) → Parrinello-Rahman / Martyna-Tuckerman (correct).

Practical tip: equilibrate with Berendsen, produce with Parrinello-Rahman.

---

## Practical MD knobs

- **Timestep** too large → energy drift / explosion. Start small.
- **Cutoff** too small → artefacts. Use tail corrections or PME for Coulomb.
- **Constraints** (SHAKE/RATTLE) for bonds to H → allows larger dt.
- **PBC + minimum image** — the infinite tiling.

