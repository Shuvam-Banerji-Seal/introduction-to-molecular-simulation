# Statistical Mechanics Bridge — Micro → Macro

> Companion note for slides 01 & 05. No derivations for their own sake — just the bridge you need to understand *why* simulation works.

## The problem

Experiments measure **macroscopic** numbers (pressure, density, heat capacity). Simulations propagate **microscopic** coordinates $\mathbf{r}^N, \mathbf{p}^N$. How do we connect them?

**Answer:** Statistical mechanics — ensemble averages.

## Ensemble average

For observable $A(\mathbf{r}^N, \mathbf{p}^N)$:

$$ \langle A \rangle = \int A(\mathbf{r}^N,\mathbf{p}^N)\, p(\mathbf{r}^N,\mathbf{p}^N)\, d\mathbf{r}^N d\mathbf{p}^N $$

where $p$ is the ensemble probability density.

| Ensemble | $p \propto$ | Fixed |
|---|---|---|
| Microcanonical (NVE) | $\delta(E - H)$ | N, V, E |
| Canonical (NVT) | $e^{-\beta U}$ | N, V, T |
| Isothermal-isobaric (NPT) | $e^{-\beta(U+PV)}$ | N, P, T |

Simulation's job: **sample $p$** via MD or MC, then estimate $\langle A\rangle$ as a time/chain average.

## Ergodic hypothesis

For ergodic systems, the **time average along a trajectory equals the ensemble average**:

$$ \bar{A}_T = \frac{1}{T}\int_0^T A(t)\,dt \;\xrightarrow[T\to\infty]{}\; \langle A\rangle $$

Caveat: ergodicity can be broken (glasses, strong barriers) — then sampling is incomplete and averages are wrong. Enhanced sampling exists for this reason.

## Partition function → everything

$$ Z = \int e^{-\beta H} d\mathbf{r}^N d\mathbf{p}^N,\qquad F = -k_BT\ln Z $$

Derivatives of $F$ give pressure, entropy, chemical potential. Free-energy differences ($\Delta F$) are the goal of many advanced simulations.

## What this means in practice

- Choose the ensemble that matches the **experimental condition**.
- Run long enough that the time average **stops drifting** (convergence).
- Estimate **statistical error** — correlated samples mean $N_{\rm eff} \ll N_{\rm frames}$.
