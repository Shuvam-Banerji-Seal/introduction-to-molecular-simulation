# Integrators — How MD Moves Atoms

## Requirements

An MD integrator should be: **time-reversible, symplectic (phase-space volume preserving), stable for large-ish dt, and cheap**.

## Velocity Verlet

The workhorse:

```
r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt^2
compute F(t+dt) → a(t+dt)
v(t+dt) = v(t) + 0.5*(a(t)+a(t+dt))*dt
```

- Symplectic → bounded energy error (no long-term drift in NVE if dt is small enough).
- Needs only one force evaluation per step.

## Stability & timestep

| System (real units) | Safe dt |
|---|---|
| LJ fluid (reduced) | 0.002–0.005 |
| Atomistic with flexible bonds | 0.5–1 fs |
| With constrained X–H bonds | 2 fs |

Rule: dt ≈ 1/20 of the fastest vibrational period.

## Thermostats (NVT)

- **Langevin**: $m\dot v = F - \gamma m v + \sqrt{2\gamma k_BT m}\,R(t)$ — friction + noise, simple and robust.
- **Nosé-Hoover**: extended Hamiltonian, deterministic.
- **Stochastic velocity rescaling (Bussi)**: gentle, correct canonical sampling.

Check: velocity histogram → Maxwell–Boltzmann; temperature fluctuations → $\sigma_T/T \sim \sqrt{2/3N}$.

## Barostats (NPT)

- **Berendsen**: fast equilibration, *not* correct ensemble.
- **Parrinello-Rahman / Martyna-Tuckerman**: correct NPT.

Tip: equilibrate with Berendsen, produce with Parrinello-Rahman.

## Constraints

SHAKE/RATTLE freeze fast bonds (e.g. O–H), allowing larger dt. Essential for water.

## Further reading

- Frenkel & Smit Ch. 4–6; Tuckerman Ch. 3–4.
