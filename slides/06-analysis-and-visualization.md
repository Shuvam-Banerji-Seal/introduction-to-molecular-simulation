---
marp: true
theme: default
paginate: true
header: "06 · Analysis & Visualization"
---

# 06 — Analysis & visualization

---

## Structure — Radial Distribution Function

$$g(r) = \frac{V}{N^2}\left\langle \sum_{i\neq j} \delta(r - r_{ij})\right\rangle / (4\pi r^2)$$

- Peaks = solvation shells / coordination.
- $g(r)\to 1$ at large $r$ (uncorrelated).
- Integrates to coordination number.

*Computed in `examples/05-analysis/`.*

---

## Dynamics — MSD & diffusion

$$\mathrm{MSD}(t) = \langle |\mathbf{r}(t)-\mathbf{r}(0)|^2\rangle \;\xrightarrow{\;t\to\infty\;}\; 6Dt$$

- Log-log slope: 1 = diffusive, <1 = subdiffusive, 2 = ballistic.
- **Pitfall:** MSD needs many time origins — don't use just one.

Diffusion via Einstein or Green-Kubo (VACF integral).

---

## Thermodynamics — fluctuations are data

- Heat capacity from $\langle \delta E^2\rangle$, compressibility from $\langle \delta V^2\rangle$.
- But: **correlated samples** → effective sample size << trajectory length.
- Always estimate **statistical error**: block averaging, bootstrap, or `pymbar`.

---

## Visualization — see what you simulated

- **VMD, OVITO, PyMOL, nglview** — qualitative checks catch setup errors instantly.
- Watch the first 100 frames before trusting any number.
- Colour by velocity / force / species to spot artefacts.

> If it *looks* wrong, it *is* wrong — no amount of analysis fixes a bad setup.

---

## The three checks before you believe a result

1. **Conservation / stability** — energy drift (NVE), $\langle T\rangle$ (NVT).
2. **Convergence** — does the average stop drifting with more sampling?
3. **Reproducibility** — different seed / initial config → same answer within error?

