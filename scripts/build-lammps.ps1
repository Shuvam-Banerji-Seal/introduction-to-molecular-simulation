# ============================================================
# LAMMPS build — Windows (PowerShell) — companion to build-lammps.sh
# Target: Windows 10/11 + Visual Studio 2022 (x64) + CUDA 11.5+
# Generated from Molecule3D Workbench (Compiler Helper) +
# tuned for A100 (sm_80) / 24-core Xeon — adapt jobs/arch for your machine.
# ============================================================
# Prerequisites (run as Administrator):
#   winget install Kitware.CMake Git.Git
#   Visual Studio 2022 with "Desktop development with C++"
#   CUDA Toolkit (https://developer.nvidia.com/cuda-toolkit)
#   Microsoft MPI (msmpisetup.exe + msmpisdk.msi) for MPI=yes
# ============================================================
$ErrorActionPreference = "Stop"

if (-Not (Test-Path lammps)) {
  git clone --depth 1 --branch develop https://github.com/lammps/lammps.git lammps
}
Set-Location lammps
if (-Not (Test-Path build)) { New-Item -ItemType Directory build | Out-Null }
Set-Location build

# Configure — most + kokkos-cuda + gpu-cuda, tuned for A100
cmake -C ../cmake/presets/most.cmake `
      -C ../cmake/presets/kokkos-cuda.cmake `
      -C ../cmake/presets/gpu-cuda.cmake `
      ../cmake `
      -G "Visual Studio 17 2022" -A x64 `
      -D CMAKE_BUILD_TYPE=Release `
      -D BUILD_MPI=yes `
      -D BUILD_OMP=yes `
      -D PKG_OPENMP=yes `
      -D PKG_GPU=yes -D GPU_API=cuda -D GPU_ARCH=sm_80 -D GPU_PREC=mixed `
      -D PKG_KOKKOS=yes -D Kokkos_ENABLE_CUDA=yes -D Kokkos_ENABLE_OPENMP=yes -D Kokkos_ARCH_AMPERE80=yes `
      -D FFT=FFTW3 -D FFT_KOKKOS=CUFFT `
      -D WITH_GZIP=yes -D WITH_JPEG=yes -D WITH_PNG=yes

# Build — use all logical cores (edit -j for your machine)
cmake --build . --config Release --parallel 24

.\bin\lmp.exe -h | Select-Object -First 80
Write-Host "Build complete. Binary: $(Resolve-Path .\bin\lmp.exe)"
