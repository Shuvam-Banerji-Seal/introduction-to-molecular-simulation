#!/usr/bin/env python3
"""
Generic LAMMPS dump (custom) -> MP4 renderer
- Reads LAMMPS dump with: ITEM: TIMESTEP / NUMBER OF ATOMS / BOX BOUNDS / ATOMS id type x y z
- Renders 3D scatter with matplotlib, saves PNG frames, compiles with ffmpeg
- Works for any lj box size, auto-scales
Usage:
  python render_lammpstrj.py --dump trajectory.lammpstrj --out video.mp4 --stride 1 --fps 15 --title "Ideal Gas"
  python render_lammpstrj.py --npz traj.npz --out video.mp4 --mode 2d --fps 15  (for python toy)
"""
import argparse, pathlib, re, subprocess, sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parse_lammpstrj(path, stride=1):
    """Yield (step, box, positions) where box=[[xlo,xhi],[ylo,yhi],[zlo,zhi]], positions Nx3"""
    with open(path, 'r') as f:
        data = f.read().splitlines()
    i=0
    frames=[]
    step_regex = re.compile(r'ITEM: TIMESTEP')
    while i < len(data):
        if data[i].strip() == 'ITEM: TIMESTEP':
            step = int(data[i+1].strip())
            # NUMBER OF ATOMS
            assert data[i+2].strip() == 'ITEM: NUMBER OF ATOMS'
            n = int(data[i+3].strip())
            assert data[i+4].strip().startswith('ITEM: BOX BOUNDS')
            box = []
            for b in range(3):
                lo,hi = map(float, data[i+5+b].split()[:2])
                box.append([lo,hi])
            # ATOMS header
            hdr = data[i+8].strip()
            # expecting id type x y z (maybe xs ys zs, but we use x y z)
            assert hdr.startswith('ITEM: ATOMS')
            cols = hdr.split()[2:]  # after ITEM: ATOMS
            # find indices
            try:
                idx_x = cols.index('x')
                idx_y = cols.index('y')
                idx_z = cols.index('z')
            except ValueError:
                # try xs, ys, zs -> convert to x = xs*box etc later? fallback use x
                idx_x = cols.index('xs') if 'xs' in cols else 2
                idx_y = cols.index('ys') if 'ys' in cols else 3
                idx_z = cols.index('zs') if 'zs' in cols else 4
                is_scaled=True
            else:
                is_scaled=False
            # read n atoms
            pos=[]
            for k in range(n):
                line = data[i+9+k]
                parts = line.split()
                # parts aligned with cols; offset 0 is id etc.
                # we have id type x y z -> parts[2],3,4 are x y z
                # generic: map cols index -> parts index
                x = float(parts[idx_x])
                y = float(parts[idx_y])
                z = float(parts[idx_z])
                if is_scaled:
                    # scaled -> real
                    x = box[0][0] + x*(box[0][1]-box[0][0])
                    y = box[1][0] + y*(box[1][1]-box[1][0])
                    z = box[2][0] + z*(box[2][1]-box[2][0])
                pos.append([x,y,z])
            frames.append((step, np.array(box), np.array(pos)))
            i = i+9+n
        else:
            i+=1
    # stride
    if stride>1:
        frames = frames[::stride]
    return frames

def render_3d(frames, out_mp4, fps=15, title="LAMMPS", point_size=18, elev=20, azim=-60, dpi=150, preview=False):
    tmpdir = pathlib.Path(out_mp4).parent / "_frames"
    tmpdir.mkdir(parents=True, exist_ok=True)
    # clean old
    for p in tmpdir.glob("frame_*.png"):
        p.unlink()
    # Determine global bounds for consistent axis
    all_boxes = np.array([f[1] for f in frames])
    # use first frame box for axis limits (assume constant NVT/NVE)
    box0 = frames[0][1]
    xlo,xhi = box0[0]
    ylo,yhi = box0[1]
    zlo,zhi = box0[2]
    # color by z height for depth cue
    for idx,(step,box,pos) in enumerate(frames):
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111, projection='3d')
        # set limits tight to box
        ax.set_xlim(xlo,xhi)
        ax.set_ylim(ylo,yhi)
        ax.set_zlim(zlo,zhi)
        # scatter
        # color gradient by z for visual depth
        colors = pos[:,2]
        sc = ax.scatter(pos[:,0], pos[:,1], pos[:,2], c=colors, cmap='cool', s=point_size, alpha=0.9, edgecolors='k', linewidths=0.2)
        ax.view_init(elev=elev, azim=azim)
        # cosmetics dark theme matching talk
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.xaxis.pane.set_facecolor('black')
        ax.yaxis.pane.set_facecolor('black')
        ax.zaxis.pane.set_facecolor('black')
        ax.grid(False)
        # tick colors
        ax.tick_params(colors='white', labelsize=6)
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        ax.set_xlabel('x', color='cyan', fontsize=8)
        ax.set_ylabel('y', color='cyan', fontsize=8)
        ax.set_zlabel('z', color='cyan', fontsize=8)
        fig.suptitle(f"{title} — step {step}", color='cyan', fontsize=11, fontweight='bold', y=0.98)
        # add box wireframe
        # draw edges of box
        corners = [
            (xlo,ylo,zlo),(xhi,ylo,zlo),(xhi,yhi,zlo),(xlo,yhi,zlo),
            (xlo,ylo,zhi),(xhi,ylo,zhi),(xhi,yhi,zhi),(xlo,yhi,zhi)
        ]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        for a,b in edges:
            ax.plot([corners[a][0],corners[b][0]],[corners[a][1],corners[b][1]],[corners[a][2],corners[b][2]], color='white', linewidth=0.6, alpha=0.5)
        ax.set_box_aspect([xhi-xlo, yhi-ylo, zhi-zlo])
        plt.tight_layout(pad=0.5)
        out_png = tmpdir / f"frame_{idx:04d}.png"
        fig.savefig(out_png, dpi=dpi, facecolor=fig.get_facecolor())
        plt.close(fig)
        if idx%20==0:
            print(f"  rendered {idx+1}/{len(frames)} -> {out_png.name}")
    # compile with ffmpeg
    print(f"[render] compiling {len(frames)} frames -> {out_mp4} at {fps} fps")
    cmd = ["ffmpeg","-y","-framerate",str(fps),"-i",str(tmpdir / "frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-vf","scale=trunc(iw/2)*2:trunc(ih/2)*2",str(out_mp4)]
    print(" ", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"[render] done {out_mp4}  size {pathlib.Path(out_mp4).stat().st_size/1024:.1f} KB")
    # keep frames for debugging, optionally clean
    # for preview we keep
    if preview:
        # also copy first frame as preview png
        import shutil
        shutil.copy(tmpdir/"frame_0000.png", pathlib.Path(out_mp4).with_suffix(".png"))
    return out_mp4

def render_2d_npz(npz_path, out_mp4, fps=15, title="Water freezing", dpi=150):
    """npz contains pos: (T,N,2) and box L, maybe temps"""
    data = np.load(npz_path)
    pos = data['pos']  # (frames,N,2)
    Lx = float(data['Lx']) if 'Lx' in data else float(data['L']) if 'L' in data else 10.0
    Ly = float(data['Ly']) if 'Ly' in data else Lx
    temps = data['temps'] if 'temps' in data else None
    frames = pos.shape[0]
    tmpdir = pathlib.Path(out_mp4).parent / "_frames2d"
    tmpdir.mkdir(parents=True, exist_ok=True)
    for p in tmpdir.glob("frame_*.png"):
        p.unlink()
    # For hexagonal coloring, compute psi6 if available
    for idx in range(frames):
        p = pos[idx]  # N,2
        fig, ax = plt.subplots(figsize=(6,6))
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        # compute local order? simple color by neighbor count via distance
        # Use cmap based on psi6 if provided else uniform
        if 'psi6' in data:
            colors = data['psi6'][idx]
            sc = ax.scatter(p[:,0], p[:,1], c=colors, cmap='RdYlBu', s=28, alpha=0.95, edgecolors='white', linewidths=0.3, vmin=0, vmax=1)
            cbar = plt.colorbar(sc, ax=ax, shrink=0.8)
            cbar.set_label(r'$\psi_6$ order', color='white')
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        else:
            sc = ax.scatter(p[:,0], p[:,1], c='#00ffff', s=30, alpha=0.9, edgecolors='white', linewidths=0.3)
        ax.set_xlim(0, Lx)
        ax.set_ylim(0, Ly)
        ax.set_aspect('equal')
        ax.tick_params(colors='white', labelsize=7)
        ax.set_xlabel('x', color='cyan', fontsize=9)
        ax.set_ylabel('y', color='cyan', fontsize=9)
        temp_label = f" — T*={temps[idx]:.2f}" if temps is not None else ""
        ax.set_title(f"{title} — frame {idx}{temp_label}", color='cyan', fontsize=11, fontweight='bold')
        # grid faint
        ax.grid(True, color='gray', alpha=0.2, linewidth=0.4)
        # box
        rect = plt.Rectangle((0,0), Lx, Ly, fill=False, edgecolor='white', linewidth=1.2, alpha=0.6)
        ax.add_patch(rect)
        plt.tight_layout(pad=0.6)
        out_png = tmpdir / f"frame_{idx:04d}.png"
        fig.savefig(out_png, dpi=dpi, facecolor=fig.get_facecolor())
        plt.close(fig)
        if idx%100==0:
            print(f" 2d rendered {idx+1}/{frames}")
    cmd = ["ffmpeg","-y","-framerate",str(fps),"-i",str(tmpdir / "frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-vf","scale=trunc(iw/2)*2:trunc(ih/2)*2",str(out_mp4)]
    print(" ", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"[render2d] done {out_mp4}")
    return out_mp4

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", help="lammpstrj path")
    ap.add_argument("--npz", help="npz path for 2D")
    ap.add_argument("--out", required=True)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--title", default="LAMMPS")
    ap.add_argument("--point_size", type=int, default=18)
    ap.add_argument("--azim", type=float, default=-60)
    ap.add_argument("--elev", type=float, default=20)
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()
    if args.dump:
        frames = parse_lammpstrj(args.dump, stride=args.stride)
        print(f"parsed {len(frames)} frames from {args.dump}, N={len(frames[0][2])}, box={frames[0][1].tolist()}")
        render_3d(frames, args.out, fps=args.fps, title=args.title, point_size=args.point_size, azim=args.azim, elev=args.elev, dpi=args.dpi)
    elif args.npz:
        render_2d_npz(args.npz, args.out, fps=args.fps, title=args.title, dpi=args.dpi)
    else:
        ap.error("need --dump or --npz")

if __name__ == "__main__":
    main()
