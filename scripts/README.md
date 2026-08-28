# LAMMPS Build Scripts — Host-tuned

These scripts generate a **full-feature LAMMPS binary on this host** (24-core Xeon Silver 4310 + NVIDIA A100) and are **cross-platform by design**.

## How the scripts were derived

1. **Live generation from your own LAMMPS Web GUI** (`https://shuvam-banerji-seal.github.io/lammps-web-gui/`):
   - Playwright navigated to **Compiler Helper** (see screenshot in `webgui-evidence/`).
   - Settings: `OS=Linux`, `Preset=Most packages (68 pkgs)`, `Accelerator=NVIDIA KOKKOS/CUDA`, `jobs=24`.
   - Copied the generated `build.sh` to `webgui-evidence/build-from-webgui.sh` (verbatim, with `Kokkos_ARCH_VOLTA70`).

2. **Local tuning for the actual hardware in this workspace**:
   - Patched `VOLTA70 → AMPERE80` for the A100 (`sm_80`, CC 8.0) — detected via `nvidia-smi` / `nvcc`.
   - Added `GPU` package alongside `KOKKOS` (`GPU_API=cuda`, `GPU_ARCH=sm_80`) so both `/gpu` and `/kk` suffix styles are available.
   - Set `FFT_KOKKOS=CUFFT` (Kokkos-CUDA needs CUFFT, not KISS).
   - Kept `most` preset + `kokkos-cuda.cmake` + `gpu-cuda.cmake` presets, plus explicit flags for `OPENMP`, `OPT`, `INTEL` to use all CPU cores.
   - `cmake --build --parallel 24` (matches `nproc`).

## Files

| File | Purpose |
|---|---|
| `build-lammps.sh` | **Linux** (bash) — run on this host or any Debian/Ubuntu with CUDA + MPI |
| `build-lammps.ps1` | **Windows** (PowerShell) — Visual Studio 17 2022 + CUDA + optional MS-MPI |
| `webgui-evidence/build-from-webgui.sh` | Verbatim script captured from the Web GUI (before local tuning) |
| `webgui-evidence/*.png` | Screenshot of the Compiler Helper interaction |

## Usage

```bash
# Linux (from repo root)
./scripts/build-lammps.sh           # clones lammps/ if needed, configures & builds with 24 cores + A100
./lammps/build/lmp -h | head        # sanity check
mpirun -np 4 ./lammps/build/lmp -in in.lj   # example

# Windows (PowerShell, x64 Native Tools)
./scripts/build-lammps.ps1
.\lammps\build\bin\lmp.exe -h
```

## Hardware adaptation

- **Different GPU?** Edit `GPU_ARCH` and `Kokkos_ARCH_*`:
  - A100 → `sm_80` / `AMPERE80` (this repo's default)
  - V100 → `sm_70` / `VOLTA70`
  - RTX 4090 / H100 → `sm_89` / `ADA89` or `sm_90` / `HOPPER90`
- **Fewer cores?** Change `--parallel 24` to `nproc` or your core count.
- **No GPU?** Drop `GPU`/`KOKKOS` lines, keep `most` + `OPENMP`.

All CPU cores are used via `BUILD_OMP=yes` + `PKG_OPENMP` + `Kokkos_ENABLE_OPENMP` + `mpirun -np`.
GPU is used via `PKG_GPU` (CUDA, mixed precision) + `PKG_KOKKOS` (CUDA, AMPERE80).
