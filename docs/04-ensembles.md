# Ensembles — Choosing the Right Thermodynamic Container

## Quick reference

| Ensemble | Fixed | Fluctuates | Use when |
|---|---|---|---|
| NVE | N,V,E | T,P | Testing integrator, true microcanonical |
| NVT | N,V,T | E,P | Slit pores, interfaces, fixed density |
| NPT | N,P,T | E,V | Most lab conditions (1 atm, 298 K) |
| μVT | μ,V,T | N,E,P | Adsorption, grand-canonical MC |

## Temperature in simulation

From equipartition:

$$ \left\langle \tfrac12 m v^2 \right\rangle = \tfrac32 k_BT $$

Instantaneous $T(t)$ fluctuates; the average should match the target. Validate the full distribution, not just the mean.

## Pressure in simulation

Virial expression:

$$ P = \rho k_BT + \frac{1}{3V}\left\langle \sum_i \mathbf{r}_i\cdot\mathbf{F}_i \right\rangle + P_{\rm tail} $$

$P_{\rm tail}$: long-range correction for truncated LJ. Without it, pressure is systematically off.

## Free energy

Not a direct average — requires thermodynamic integration, FEP, umbrella sampling, or MBAR.

If your question is "which state is more stable?" or "what is the binding affinity?", you need a free-energy method.

## Checklist

- [ ] Ensemble matches the experimental condition for the observable.
- [ ] Thermostat/barostat + parameters reported (reproducibility).
- [ ] Equilibration monitored (T, P, E, density plateau).
- [ ] Fluctuations scale as $1/\sqrt{N}$ (sanity check).
