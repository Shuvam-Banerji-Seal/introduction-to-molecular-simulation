# Simulations — Quick LAMMPS Demos with GPU + Video

Three small molecular simulations that run in **<6 minutes each** on the A100 GPU and produce trajectory videos. All use **LAMMPS** (built from source with GPU+CUDA support) and reduced LJ units.

## Quick run

```bash
# From repo root, using the locally-built LAMMPS binary:
LMP=./lammps/build/lmp

# Run all 3 simulations (GPU-accelerated):
$LMP -sf gpu -pk gpu 1 neigh no -in simulations/01-ideal-gas/in.ideal-gas.lammps
$LMP -sf gpu -pk gpu 1 neigh no -in simulations/02-lj-freezing/in.freezing.lammps
$LMP -sf gpu -pk gpu 1 neigh no -in simulations/03-water-ice-freezing/in.water-ice.lammps

# Render videos from trajectories:
python3 simulations/render_lammpstrj.py --dump simulations/01-ideal-gas/trajectory.lammpstrj --out videos/01-ideal-gas.mp4 --fps 15 --title "Ideal Gas"
python3 simulations/render_lammpstrj.py --dump simulations/02-lj-freezing/trajectory.lammpstrj --out videos/02-lj-freezing.mp4 --fps 15 --title "LJ Freezing"
python3 simulations/render_lammpstrj.py --dump simulations/03-water-ice-freezing/trajectory.lammpstrj --out videos/03-water-ice-freezing.mp4 --fps 15 --title "Water-Ice Freezing"
```

## Simulations

| # | Name | N atoms | Ensemble | T quench | Steps | Physics | Video |
|---|------|---------|----------|----------|-------|---------|-------|
| 01 | **Ideal Gas** | 380 | NVE | T*=2.0 (constant) | 2000 | Dilute LJ gas (ρ=0.047, ε=0.2), ballistic motion, rare collisions | `videos/01-ideal-gas.mp4` (1.6 MB, 6.7s) |
| 02 | **LJ Freezing** | 864 | NVT | 3.0 → 0.3 | 2000 | Dense LJ fluid (ρ=0.844) crystallizes into FCC on quench | `videos/02-lj-freezing.mp4` (1.7 MB, 6.7s) |
| 03 | **Water-Ice Freezing** | 864 | NVT | 2.0 → 0.1 | 3000 | Deep quench of dense LJ fluid — analog of water→ice | `videos/03-water-ice-freezing.mp4` (1.8 MB, 6.7s) |

## GPU acceleration

All simulations use the LAMMPS GPU package (`-sf gpu -pk gpu 1`):

```
GPU package API: CUDA
GPU package precision: mixed
GPU arch: sm_80 (A100 Ampere)
```

The A100 is shared (49 GB used by other process), but 36 GB free is plenty for these small systems.

## File structure

```
simulations/
├── render_lammpstrj.py              # Shared renderer: LAMMPS dump → MP4 (3D scatter, dark theme)
├── 01-ideal-gas/
│   ├── in.ideal-gas.lammps          # LAMMPS input script
│   ├── trajectory.lammpstrj          # Trajectory (100 frames)
│   └── log.lammps                    # Thermo log
├── 02-lj-freezing/
│   ├── in.freezing.lammps
│   ├── trajectory.lammpstrj          # 101 frames
│   └── log.lammps
└── 03-water-ice-freezing/
    ├── in.water-ice.lammps
    ├── trajectory.lammpstrj          # 101 frames
    ├── log.lammps
    └── water_freezing.py             # (legacy Python toy — superseded by LAMMPS version)

videos/
├── 01-ideal-gas.mp4                  # 1200×900, h264, 6.7s
├── 02-lj-freezing.mp4                # 1200×900, h264, 6.7s
└── 03-water-ice-freezing.mp4         # 1200×900, h264, 6.7s
```

## Key physics observed

### 01 — Ideal Gas
- T stable at ~1.75 (NVE, no thermostat), E_total conserved at ~2.59
- Pressure ≈ ρT = 0.047 × 1.75 ≈ 0.082 (ideal gas law holds)
- Atoms move ballistically with rare collisions (low density)

### 02 — LJ Freezing
- T quenched from 3.0 → 0.3 over 1500 steps
- PE drops from -3.6 → -5.1 (more negative = more ordered)
- Pressure drops from 12 → 0.4 (liquid → solid transition)
- FCC crystal forms at low T

### 03 — Water-Ice Freezing (deep quench)
- T quenched from 2.0 → 0.1 over 2500 steps
- PE drops from -4.4 → -6.2 (strong crystallization)
- Pressure drops from 7.6 → -2.4 (negative pressure = solid under tension)
- Deep quench ensures complete crystal formation
