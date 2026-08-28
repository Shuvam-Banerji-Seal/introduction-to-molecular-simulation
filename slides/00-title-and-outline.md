---
marp: true
theme: default
paginate: true
header: "Introduction to Molecular Simulation"
footer: "Shuvam Banerji Seal — 2026"
---

# Introduction to Molecular Simulation

### What it is, why it works, and how to run one

**Shuvam Banerji Seal** · 2026

> Companion repo: `github.com/Shuvam-Banerji-Seal/introduction-to-molecular-simulation`

---

## Outline

1. **What is molecular simulation?** — the micro → macro bridge
2. **Potentials & force fields** — what moves atoms
3. **Molecular Dynamics** — integrating Newton's equations
4. **Monte Carlo** — importance sampling & Metropolis
5. **Ensembles & thermodynamics** — NVE / NVT / NPT, thermostat, barostat
6. **Analysis & visualization** — RDF, MSD, free energies, pitfalls
7. **How to make a simulation** — 7-step live workflow

*Each section has a runnable example in `examples/`.*

---

## How to use these slides

- Written in **Marp Markdown** — renders on GitHub, exports to PDF/PPTX/HTML.
- Present with VS Code Marp extension or: `marp slides/ --pdf`
- Speaker notes are in HTML comments (`<!-- -->`) — visible in presenter view.
- Deeper notes live in `docs/` (one file per section).

<!--
Speaker note: set expectations — no prior MD/MC needed, basic stat mech & Python helpful.
Poll the room: who has run a simulation before?
-->
