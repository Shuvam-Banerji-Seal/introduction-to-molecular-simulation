#!/usr/bin/env bash
# ============================================================
# LAMMPS build — Introduction to Molecular Simulation companion
# Generated from LAMMPS Web GUI (Molecule3D Workbench by Shuvam
# Banerji Seal) + local tuning for this host:
#   CPU: Intel Xeon Silver 4310 (24 cores, 2 sockets, AVX-512)
#   GPU: NVIDIA A100 80GB PCIe (Ampere, sm_80, CC 8.0)
#   OS: Ubuntu 22.04 LTS (Jammy) — Debian/Ubuntu family
#   CUDA: 13.3 (with 12.9 fallback) — nvcc 13.3 at /usr/local/cuda-13.3/bin/nvcc
#   Target: Linux (bash) — for Windows see build-lammps.ps1
# ============================================================
# Provenance:
#   1. Open https://shuvam-banerji-seal.github.io/lammps-web-gui/
#   2. Compiler Helper → OS=Linux, Preset=Most (68 pkgs), Accelerator=NVIDIA KOKKOS/CUDA, jobs=24
#   3. Captured via Playwright (webgui-evidence/build-from-webgui.sh, VOLTA70)
#   4. Locally patched: VOLTA70 → AMPERE80 (A100 sm_80), added GPU package,
#      FFT_KOKKOS=CUFFT, CUDA_ROOT=13.3, --parallel 24, OPENMP+MPI+GPU+KOKKOS
# ============================================================
set -euo pipefail
set -x

# Prefer CUDA 13.3 for Kokkos C++20 support (requires NVCC 12.2+); fallback to default nvcc
if [ -x "/usr/local/cuda-13.3/bin/nvcc" ]; then
  export PATH=/usr/local/cuda-13.3/bin:$PATH
  export CUDA_ROOT=/usr/local/cuda-13.3
elif [ -x "/usr/local/cuda-12.9/bin/nvcc" ]; then
  export PATH=/usr/local/cuda-12.9/bin:$PATH
  export CUDA_ROOT=/usr/local/cuda-12.9
fi
nvcc --version

# Clone if needed (workspace already has lammps/ via earlier clone)
if [ ! -d "lammps" ]; then
  git clone --depth 1 --branch develop https://github.com/lammps/lammps.git lammps
fi
cd lammps

# Configure — most + kokkos-cuda + gpu-cuda + host tuning for 24 cores + A100
mkdir -p build && cd build
cmake -C ../cmake/presets/most.cmake \
      -C ../cmake/presets/kokkos-cuda.cmake \
      -C ../cmake/presets/gpu-cuda.cmake \
      ../cmake \
      -D CMAKE_BUILD_TYPE=Release \
      -D BUILD_MPI=yes \
      -D BUILD_OMP=yes \
      -D BUILD_TOOLS=yes \
      -D PKG_OPENMP=yes \
      -D PKG_GPU=yes \
      -D PKG_KOKKOS=yes \
      -D PKG_INTEL=yes \
      -D PKG_OPT=yes \
      -D GPU_API=cuda \
      -D GPU_ARCH=sm_80 \
      -D GPU_PREC=mixed \
      -D Kokkos_ENABLE_CUDA=yes \
      -D Kokkos_ENABLE_OPENMP=yes \
      -D Kokkos_ARCH_AMPERE80=yes \
      -D FFT=FFTW3 \
      -D FFT_KOKKOS=CUFFT \
      -D WITH_GZIP=yes \
      -D WITH_JPEG=yes \
      -D WITH_PNG=yes \
      -D WITH_FFMPEG=yes \
      -D DOWNLOAD_VORO=yes \
      -D DOWNLOAD_EIGEN3=yes

# Build with all 24 cores
cmake --build . --parallel 24

# Optional install (needs sudo)
# sudo cmake --install .

# Sanity checks
./lmp -h 2>&1 | head -n 100
echo "=== Installed packages ==="
./lmp -h 2>&1 | grep -E "Installed|package" | head -n 100
echo "=== GPU / Kokkos ==="
./lmp -sf gpu -pk gpu 1 -h 2>&1 | grep -i gpu | head -n 20 || true
./lmp -k on g 1 -sf kk -h 2>&1 | head -n 40 || true
echo "Binary: $(pwd)/lmp"
ldd ./lmp 2>&1 | head -n 40 || true
