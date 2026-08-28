---
marp: true
theme: default
paginate: true
header: "02 · Potentials & Force Fields"
---

# 02 — Potentials & force fields

---

## Potential energy surface (PES)

- $U(\mathbf{r}^N)$ — scalar field over all atomic positions.
- Forces: $\mathbf{F}_i = -\nabla_i U$.
- Everything flows from $U$: dynamics, thermodynamics, structure.

> Choose $U$ well → results are credible. Choose poorly → beautifully wrong.

---

## Lennard-Jones — the "hydrogen atom" of simulation

$$U_{\mathrm{LJ}}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

- $\sigma$ — length scale (excluded volume), $\varepsilon$ — energy scale.
- $r^{-6}$: dispersion (attraction), $r^{-12}$: Pauli repulsion (convenient, not fundamental).
- Reduced units: $r^*=r/\sigma,\; T^*=k_BT/\varepsilon$ — makes the toy universal.

*Live example: `examples/01-lennard-jones-fluid/`*

---

## From LJ to a force field

```
Bonded:     bonds, angles, dihedrals  (harmonic / cosine)
Non-bonded: LJ + Coulomb              (long-range → Ewald / PME)
```

Families: **AMBER, CHARMM, OPLS, GROMOS** (biomolecular), **ReaxFF, EAM, ML potentials** (materials).

Mixing rules, cutoffs, long-range corrections — details matter.

---

## Choosing a force field — checklist

- [ ] Validated for **your chemistry** (proteins ≠ polymers ≠ metals)?
- [ ] Water model consistent with it (TIP3P vs TIP4P vs OPC)?
- [ ] Cutoff & long-range method match the parametrization?
- [ ] Units consistent? (kcal/mol vs kJ/mol — the classic trap)

> When in doubt, reproduce a known pure-liquid property (density, $\Delta H_{\rm vap}$).

---

## Modern direction: Machine-Learned Potentials

- Learn $U(\mathbf{r})$ from ab initio data (DFT/CC) → near-quantum accuracy, MD speed.
- Examples: ANI, MACE, NequIP, CHGNet.
- Still need careful validation & uncertainty — not magic.

*Next: how we propagate the system — MD.*
