---
marp: true
theme: default
paginate: true
header: "04 · Monte Carlo"
---

# 04 — Monte Carlo

---

## The idea: importance sampling

Instead of integrating over all configurations, **sample them with probability** $p \propto e^{-\beta U}$.

We generate a Markov chain whose stationary distribution *is* the Boltzmann distribution.

No forces needed — only **energies**.

---

## Metropolis rule

1. Propose a move: $\mathbf{r} \to \mathbf{r}'$ (e.g. displace one particle).
2. Compute $\Delta U = U(\mathbf{r}') - U(\mathbf{r})$.
3. Accept with probability:

$$P_{\rm acc} = \min\!\left(1, e^{-\beta \Delta U}\right)$$

- $\Delta U < 0$ → always accept. $\Delta U > 0$ → accept sometimes (thermal fluctuations).

*Demo: `examples/03-monte-carlo-lj/run.py`*

---

## What makes a good MC move?

- **Ergodic** — can reach all relevant states.
- **Detailed balance** — $p(\mathbf{r})\,T(\mathbf{r}\!\to\!\mathbf{r}') = p(\mathbf{r}')\,T(\mathbf{r}'\!\to\!\mathbf{r})$.
- **Tunable acceptance** — aim ~20–50% (adjust step size).
- Clever moves (cluster, swap, CBMC) beat brute force for dense / polymeric systems.

---

## MD vs MC — when to use which?

| Need | Prefer |
|---|---|
| Dynamics, transport, spectra | MD |
| Phase coexistence, high barriers | MC (or enhanced sampling) |
| No forces available | MC |
| Free energy via alchemy | Either (+ thermodynamic integration / MBAR) |

In practice: **use the tool that samples fastest for your observable**.

