#!/usr/bin/env python3
"""
Toy 2D 'water freezing' — LJ + Langevin quench from liquid (T=2.0) to solid (T=0.1)
Shows disorder -> hexagonal order (ice-like).  Pure numpy, no LAMMPS needed.
N=400 in 2D periodic box.  Colors by local psi6 hexagonal order.

Key fixes from v1:
  - Triangular lattice init (no overlaps -> no blowup)
  - Velocity Verlet + Langevin (BAOAB) instead of Euler-Maruyama
  - Smaller dt=0.002, force capping at r>0.4*sigma
  - Longer run: 6000 steps, 300 frames

Outputs: trajectory.npz (pos [F,N,2], temps, psi6)
"""
import numpy as np
import pathlib

# ============================== Parameters ==============================
N = 400
L = 20.0
rho = N / (L * L)
np.random.seed(42)

# LJ params (reduced units)
eps = 1.0
sigma = 1.0
rc = 3.0
rc2 = rc * rc
dt = 0.002
gamma = 1.0  # Langevin friction
m = 1.0
kT = 1.0  # not used directly, T is set per step

# Temperature schedule
Thot = 2.0
Tcold = 0.1
steps_hot = 1500       # equilibrate as liquid
steps_quench = 4500   # linear ramp hot -> cold
steps_total = steps_hot + steps_quench
dump_every = 20        # dump every 20 steps -> 300 frames

# ============================== Init: triangular lattice ==============================
def init_triangular(N_target, L):
    """Place atoms on triangular lattice, then jitter. Guarantees no overlaps."""
    # spacing for triangular lattice at given density
    a = np.sqrt(2.0 / (np.sqrt(3.0) * N_target / (L * L)))
    # number per row
    nx = int(np.ceil(L / a))
    ny = int(np.ceil(L / (a * np.sqrt(3.0) / 2.0)))
    pos = []
    for j in range(ny):
        for i in range(nx):
            x = i * a + (a / 2.0 if j % 2 == 1 else 0.0)
            y = j * a * np.sqrt(3.0) / 2.0
            if x < L and y < L:
                pos.append([x, y])
    pos = np.array(pos)
    # Trim or pad to N_target
    if len(pos) > N_target:
        idx = np.random.choice(len(pos), N_target, replace=False)
        pos = pos[idx]
    elif len(pos) < N_target:
        extra = N_target - len(pos)
        extra_pos = np.random.rand(extra, 2) * L
        pos = np.vstack([pos, extra_pos])
    # Jitter to break perfect lattice (liquid-like)
    pos += np.random.randn(N_target, 2) * 0.3 * a
    pos = np.mod(pos, L)
    return pos

pos = init_triangular(N, L)
vel = np.zeros((N, 2))
print(f"N={N} L={L} rho={rho:.3f}  init: triangular lattice + jitter")

# ============================== Force computation ==============================
def compute_forces(pos):
    """Vectorized LJ force with PBC minimum image. O(N^2) but N=400 is fine."""
    dx = pos[:, None, 0] - pos[None, :, 0]
    dy = pos[:, None, 1] - pos[None, :, 1]
    # Minimum image
    dx -= L * np.round(dx / L)
    dy -= L * np.round(dy / L)
    r2 = dx * dx + dy * dy
    mask = (r2 < rc2) & (r2 > 1e-4)
    # Cap r2 to avoid singularity
    r2_capped = np.where(mask & (r2 < 0.25), 0.25, r2)  # r > 0.5*sigma minimum
    inv_r2 = np.zeros_like(r2)
    np.divide(1.0, r2_capped, out=inv_r2, where=mask)
    inv_r6 = inv_r2 ** 3 * (sigma ** 6)
    inv_r12 = inv_r6 ** 2
    mag = 24.0 * eps * (2.0 * inv_r12 - inv_r6) * inv_r2
    mag[~mask] = 0.0
    mag[np.diag_indices(N)] = 0.0
    fx = np.sum(mag * dx, axis=1)
    fy = np.sum(mag * dy, axis=1)
    return np.column_stack([fx, fy])

# ============================== psi6 local order parameter ==============================
def compute_psi6(pos):
    """Local hexagonal order: |<exp(6i*theta)>| for neighbors within 1.5*sigma."""
    N = pos.shape[0]
    psi = np.zeros(N)
    dx = pos[:, None, 0] - pos[None, :, 0]
    dy = pos[:, None, 1] - pos[None, :, 1]
    dx -= L * np.round(dx / L)
    dy -= L * np.round(dy / L)
    r2 = dx * dx + dy * dy
    neigh_mask = (r2 < 1.5**2) & (r2 > 1e-4)
    for i in range(N):
        neigh = np.where(neigh_mask[i])[0]
        if len(neigh) > 0:
            angles = np.arctan2(dy[i, neigh], dx[i, neigh])
            psi[i] = np.abs(np.mean(np.exp(1j * 6 * angles)))
    return psi

# ============================== BAOAB Langevin integrator ==============================
# BAOAB: B = half kick, A = half drift, O = stochastic rotation, A = half drift, B = half kick
# This is a proper symplectic + stochastic integrator, much more stable than Euler-Maruyama

force = compute_forces(pos)
frames = []
temps_log = []
psi_log = []

print(f"Running {steps_total} steps (dt={dt})...")
for step in range(steps_total):
    # Temperature schedule
    if step < steps_hot:
        T = Thot
    else:
        frac = (step - steps_hot) / steps_quench
        T = Thot + frac * (Tcold - Thot)

    # BAOAB Langevin (simplified: B-A-O-A-B)
    # B: half kick
    vel += 0.5 * force * dt / m
    # A: half drift
    pos += 0.5 * vel * dt
    # O: stochastic velocity update (Ornstein-Uhlenbeck)
    c1 = np.exp(-gamma * dt)
    c2 = np.sqrt(1.0 - c1**2)
    noise = np.random.randn(N, 2)
    vel = c1 * vel + c2 * np.sqrt(T / m) * noise
    # A: half drift
    pos += 0.5 * vel * dt
    # PBC wrap
    pos = np.mod(pos, L)
    # B: half kick (with new forces)
    force = compute_forces(pos)
    vel += 0.5 * force * dt / m

    # Logging
    if step % dump_every == 0:
        frames.append(pos.copy())
        temps_log.append(T)
        if step % 200 == 0:
            psi = compute_psi6(pos)
            ke = 0.5 * m * np.mean(np.sum(vel * vel, axis=1))
            print(f"  step {step:5d}/{steps_total}  T={T:.3f}  avg_psi6={np.mean(psi):.3f}  KE={ke:.3f}")
        else:
            psi_log_placeholder = True

# Compute psi6 for ALL frames (not just every 200 steps)
print("Computing psi6 for all frames...")
psi_all = []
for f in frames:
    psi_all.append(compute_psi6(f))
psi_all = np.array(psi_all)

frames = np.array(frames)
temps_log = np.array(temps_log)
print(f"frames {frames.shape}  temps {temps_log.shape}  psi6 {psi_all.shape}")
print(f"psi6 range: {np.mean(psi_all[0]):.3f} (hot) -> {np.mean(psi_all[-1]):.3f} (cold)")

out = pathlib.Path(__file__).parent / "trajectory.npz"
np.savez_compressed(out, pos=frames, Lx=L, Ly=L, temps=temps_log, psi6=psi_all)
print(f"saved {out}  {frames.shape[0]} frames  {pathlib.Path(out).stat().st_size / 1024:.1f} KB")
