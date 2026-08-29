#!/usr/bin/env python3
"""
2D LAMMPS trajectory renderer with local hexagonal order (psi6) coloring.

- Reads LAMMPS dump (custom) with: id type x y z
- Projects to 2D (xy plane), computes local psi6 per atom per frame
- Colors: blue (disordered, psi6~0) -> red (crystalline, psi6~1)
- Shows temperature from thermo log if available
- Renders PNG frames, compiles with ffmpeg to MP4

Usage:
  python render_2d.py --dump trajectory.lammpstrj --out video.mp4 --fps 15 --title "LJ Freezing"
  python render_2d.py --dump trajectory.lammpstrj --out video.mp4 --fps 15 --title "Ideal Gas" --psi6 false
  python render_2d.py --dump trajectory.lammpstrj --out video.mp4 --log log.lammps --title "Water-Ice"
"""
import argparse, pathlib, re, subprocess, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def parse_lammpstrj(path, stride=1):
    """Yield (step, box, positions_xy) where positions is Nx2"""
    with open(path, 'r') as f:
        data = f.read().splitlines()
    i = 0
    frames = []
    while i < len(data):
        if data[i].strip() == 'ITEM: TIMESTEP':
            step = int(data[i+1].strip())
            assert data[i+2].strip() == 'ITEM: NUMBER OF ATOMS'
            n = int(data[i+3].strip())
            assert data[i+4].strip().startswith('ITEM: BOX BOUNDS')
            box = []
            for b in range(3):
                parts = data[i+5+b].split()
                lo, hi = float(parts[0]), float(parts[1])
                box.append([lo, hi])
            hdr = data[i+8].strip()
            assert hdr.startswith('ITEM: ATOMS')
            cols = hdr.split()[2:]
            idx_x = cols.index('x')
            idx_y = cols.index('y')
            pos = []
            for k in range(n):
                parts = data[i+9+k].split()
                x = float(parts[idx_x])
                y = float(parts[idx_y])
                pos.append([x, y])
            frames.append((step, np.array(box), np.array(pos)))
            i = i + 9 + n
        else:
            i += 1
    if stride > 1:
        frames = frames[::stride]
    return frames

def parse_thermo_log(log_path):
    """Parse LAMMPS log for step -> temperature mapping."""
    if not log_path or not pathlib.Path(log_path).exists():
        return {}
    temps = {}
    with open(log_path, 'r') as f:
        lines = f.readlines()
    # Find thermo data lines: lines that start with whitespace + number
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split()
        if len(parts) >= 2:
            try:
                step = int(parts[0])
                temp = float(parts[1])
                temps[step] = temp
            except (ValueError, IndexError):
                continue
    return temps

def compute_psi6(pos, Lx, Ly, cutoff=1.5):
    """
    Local hexagonal bond-orientational order parameter.
    psi6_i = |<exp(6i*theta_ij)>| for neighbors j within cutoff.
    Returns array of N values in [0, 1].
    0 = completely disordered, 1 = perfect hexagonal crystal.
    """
    N = pos.shape[0]
    psi = np.zeros(N)
    dx = pos[:, None, 0] - pos[None, :, 0]
    dy = pos[:, None, 1] - pos[None, :, 1]
    # Minimum image
    dx -= Lx * np.round(dx / Lx)
    dy -= Ly * np.round(dy / Ly)
    r2 = dx * dx + dy * dy
    neigh_mask = (r2 < cutoff**2) & (r2 > 1e-6)
    for i in range(N):
        neigh = np.where(neigh_mask[i])[0]
        if len(neigh) > 0:
            angles = np.arctan2(dy[i, neigh], dx[i, neigh])
            psi[i] = np.abs(np.mean(np.exp(1j * 6.0 * angles)))
    return psi

def render_2d(frames, out_mp4, fps=15, title="Simulation", use_psi6=True,
              point_size=35, dpi=150, thermo_log=None, cmap='RdYlBu_r'):
    """
    Render 2D trajectory to MP4 with psi6 coloring.
    """
    tmpdir = pathlib.Path(out_mp4).parent / "_frames_2d"
    tmpdir.mkdir(parents=True, exist_ok=True)
    for p in tmpdir.glob("frame_*.png"):
        p.unlink()

    box0 = frames[0][1]
    xlo, xhi = box0[0]
    ylo, yhi = box0[1]
    Lx = xhi - xlo
    Ly = yhi - ylo

    # Parse temperature from log if available
    temp_map = parse_thermo_log(thermo_log) if thermo_log else {}

    # Custom colormap: blue (disordered) -> yellow -> red (ordered)
    if cmap == 'custom':
        colors_list = ['#2196F3', '#4FC3F7', '#FFF176', '#FF8A65', '#E53935']
        cmap_obj = mcolors.LinearSegmentedColormap.from_list('psi6', colors_list, N=256)
    else:
        cmap_obj = plt.get_cmap(cmap)

    N = frames[0][2].shape[0]
    print(f"Rendering {len(frames)} frames, N={N}, box={Lx:.1f}x{Ly:.1f}, psi6={use_psi6}")

    for idx, (step, box, pos) in enumerate(frames):
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor('black')
        ax.set_facecolor('#0a0a0a')

        if use_psi6:
            psi = compute_psi6(pos, Lx, Ly, cutoff=1.5)
            sc = ax.scatter(pos[:, 0], pos[:, 1], c=psi, cmap=cmap_obj,
                           s=point_size, alpha=0.95, edgecolors='white',
                           linewidths=0.3, vmin=0.0, vmax=1.0)
            cbar = plt.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
            cbar.set_label(r'$\psi_6$ (hexagonal order)', color='white', fontsize=10)
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
            cbar.outline.set_edgecolor('white')
            cbar.outline.set_linewidth(0.5)
        else:
            # Uniform color for ideal gas (no order expected)
            sc = ax.scatter(pos[:, 0], pos[:, 1], c='#00ffff',
                           s=point_size, alpha=0.9, edgecolors='white',
                           linewidths=0.3)

        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)
        ax.set_aspect('equal')
        ax.tick_params(colors='white', labelsize=7)
        ax.set_xlabel('x', color='#00ffff', fontsize=9)
        ax.set_ylabel('y', color='#00ffff', fontsize=9)

        # Temperature annotation
        temp_str = ""
        if step in temp_map:
            temp_str = f"  T*={temp_map[step]:.2f}"
        elif temp_map:
            # Find nearest step
            nearest = min(temp_map.keys(), key=lambda s: abs(s - step))
            temp_str = f"  T*~{temp_map[nearest]:.2f}"

        avg_psi = ""
        if use_psi6:
            avg_psi = f"  <ψ₆>={np.mean(psi):.3f}"

        ax.set_title(f"{title} — step {step}{temp_str}{avg_psi}",
                    color='#00ffff', fontsize=11, fontweight='bold', pad=10)

        # Faint grid
        ax.grid(True, color='gray', alpha=0.15, linewidth=0.3)

        # Box border
        rect = plt.Rectangle((xlo, ylo), Lx, Ly, fill=False,
                            edgecolor='white', linewidth=1.0, alpha=0.4)
        ax.add_patch(rect)

        plt.tight_layout(pad=0.5)
        out_png = tmpdir / f"frame_{idx:04d}.png"
        fig.savefig(out_png, dpi=dpi, facecolor=fig.get_facecolor())
        plt.close(fig)

        if idx % 30 == 0:
            extra = f" avg_psi6={np.mean(psi):.3f}" if use_psi6 else ""
            print(f"  frame {idx+1}/{len(frames)}{extra}")

    # Compile with ffmpeg
    print(f"Compiling {len(frames)} frames -> {out_mp4} at {fps} fps")
    cmd = ["ffmpeg", "-y", "-framerate", str(fps),
           "-i", str(tmpdir / "frame_%04d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
           "-crf", "18",
           str(out_mp4)]
    print("  " + " ".join(cmd))
    subprocess.run(cmd, check=True)
    size_mb = pathlib.Path(out_mp4).stat().st_size / (1024*1024)
    print(f"Done: {out_mp4} ({size_mb:.1f} MB)")
    return out_mp4

def main():
    ap = argparse.ArgumentParser(description="2D LAMMPS trajectory renderer with psi6 coloring")
    ap.add_argument("--dump", required=True, help="LAMMPS dump file")
    ap.add_argument("--out", required=True, help="Output MP4 path")
    ap.add_argument("--log", help="LAMMPS log file for temperature annotation")
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--title", default="Simulation")
    ap.add_argument("--point_size", type=int, default=35)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--psi6", default="true", help="Enable psi6 coloring (true/false)")
    ap.add_argument("--cmap", default="custom", help="Colormap: custom, RdYlBu_r, coolwarm, etc.")
    args = ap.parse_args()

    use_psi6 = args.psi6.lower() in ("true", "yes", "1")
    frames = parse_lammpstrj(args.dump, stride=args.stride)
    print(f"Parsed {len(frames)} frames, N={frames[0][2].shape[0]}")
    render_2d(frames, args.out, fps=args.fps, title=args.title,
              use_psi6=use_psi6, point_size=args.point_size,
              dpi=args.dpi, thermo_log=args.log, cmap=args.cmap)

if __name__ == "__main__":
    main()
