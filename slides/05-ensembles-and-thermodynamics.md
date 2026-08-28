---
marp: true
theme: default
paginate: true
header: "05 · Ensembles & Thermodynamics"
---

# 05 — Ensembles & thermodynamics

---

## Ensembles — the thermodynamic container

| Ensemble | Fixed | Conjugate fluctuates | When to use |
|---|---|---|---|
| **NVE** | N, V, E | T, P | Fundamental, check energy conservation |
| **NVT** | N, V, T | E, P | Confined / interfacial, thermostat |
| **NPT** | N, P, T | E, V | Most experiments (1 atm, 300 K) |
| $\mu$VT | $\mu$, V, T | N | Adsorption, grand-canonical |

> Match the ensemble to the **experimental condition** you want to compare to.

---

## Temperature & pressure — what they really are in simulation

- **Temperature** from kinetic energy: $\langle \tfrac12 m v^2 \rangle = \tfrac32 k_BT$ (equipartition).
- **Pressure** from virial: $P = \rho k_BT + \frac{1}{3V}\langle \sum_i \mathbf{r}_i\!\cdot\!\mathbf{F}_i\rangle$.

Both are **averages** — expect fluctuations that shrink as $1/\sqrt{N}$.

---

## Free energy — the "why" behind spontaneity

- $\Delta G = -k_BT \ln \frac{Z_B}{Z_A}$ — ratio of partition functions.
- Not a direct average — needs **special tricks**: thermodynamic integration, FEP, umbrella sampling, MBAR.
- Free energy → phase stability, binding affinity, solubility.

*Beyond intro scope, but you should know it exists and why it matters.*

---

## Choosing checklist

- [ ] Does my observable require NPT (e.g. density) or is NVT sufficient?
- [ ] Have I equilibrated long enough that $\langle T\rangle,\langle P\rangle,\langle E\rangle$ are stable?
- [ ] Are fluctuations physical? (Compare to $1/\sqrt{N}$ expectation)
- [ ] Have I reported **which** thermostat/barostat and its parameters?

