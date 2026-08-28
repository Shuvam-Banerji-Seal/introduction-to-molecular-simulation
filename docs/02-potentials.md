# Potentials & Force Fields

## Potential energy surface

$U(\mathbf{r}^N)$ determines forces $\mathbf{F}_i = -\nabla_i U$ and hence all dynamics and thermodynamics.

## Lennard-Jones

$$ U_{\rm LJ}(r) = 4\varepsilon\left[(\sigma/r)^{12} - (\sigma/r)^6\right] $$

- $\sigma$: onset of repulsion; $\varepsilon$: well depth.
- Minimum at $r_{\min}=2^{1/6}\sigma$, depth $-\varepsilon$.
- Reduced units: $r^*=r/\sigma$, $T^*=k_BT/\varepsilon$, $t^*=t\sqrt{\varepsilon/m\sigma^2}$.

Truncation: $U(r>r_c)=0$ with tail corrections for pressure/energy, or shifted/smoothed cutoff.

## Coulomb

$$ U_{\rm Coul}(r) = \frac{1}{4\pi\epsilon_0}\frac{q_i q_j}{r} $$

Long-ranged ($1/r$) — cannot cutoff naively. Use **Ewald / PME / PPPM**.

## Bonded terms (molecular force fields)

$$ U_{\rm bonded} = \sum_{\rm bonds} k_b(r-r_0)^2 + \sum_{\rm angles} k_\theta(\theta-\theta_0)^2 + \sum_{\rm dihedrals} V_n[1+\cos(n\phi-\gamma)] $$

Plus cross terms, impropers, etc. depending on family.

## Force-field families

| Family | Strength | Typical use |
|---|---|---|
| AMBER / CHARMM / OPLS | Biomolecules (proteins, lipids, nucleic acids) | Drug binding, membranes |
| GROMOS | United-atom biomolecules | Coarse efficiency |
| EAM / MEAM | Metals | Materials |
| ReaxFF | Reactive (bond breaking) | Catalysis, combustion |
| ML (MACE, NequIP, ANI) | Learned from QM | High accuracy, system-specific |

## Practical advice

- Never mix force-field families without validation.
- Match water model to the force field (parameterized together).
- Check units: kJ/mol vs kcal/mol, nm vs Å.
- Reproduce a known bulk property before trusting a new system.
