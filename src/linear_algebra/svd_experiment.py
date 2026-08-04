"""
SVD geometric decomposition experiment.

We pick a generic full-rank non-symmetric W in R^{2x2} and visualize
the four-step decomposition W = U Sigma V^T applied to a vector x:

    x  --(V^T)-->  V^T x  --(Sigma)-->  Sigma V^T x  --(U)-->  U Sigma V^T x = W x

All vectors are plotted on a FIXED standard-basis canvas (Model A).
Tilted V and U axes appear as visual aids only -- they never become
horizontal/vertical.
"""

# %% Imports
import os

import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLOT_DIR = os.path.join(SCRIPT_DIR, "plots")
os.makedirs(PLOT_DIR, exist_ok=True)

# %% ---------------------------------------------------------------
# Setup: choose W, x, and decompose
# ------------------------------------------------------------------
# Generic full-rank non-symmetric W -- no triangular or symmetric
# structure that would let us read singular values off the entries.
W = np.array([[2.0, 1.0], [-1.0, 3.0]])

# Input vector -- chosen off-axis so it's clearly not aligned with
# either the standard frame or (likely) the V frame.
x = np.array([1.0, 1.5])

# --- Build V from eig(W^T W), sorted descending ---
WtW = W.T @ W
eigvals, eigvecs = np.linalg.eig(WtW)

# np.linalg.eig does NOT sort. Sort descending so sigma_1 >= sigma_2.
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]

V = eigvecs  # columns are v_1, v_2
sigmas = np.sqrt(eigvals)  # sigma_i = sqrt(lambda_i)
Sigma = np.diag(sigmas)

# --- Derive U from V to keep signs consistent (Invariant 5) ---
# u_i = W v_i / sigma_i guarantees U Sigma V^T = W exactly.
U = W @ V / sigmas  # broadcasting: divides each column

# --- Verify invariants ---
print("=== Invariant checks ===")
print(f"W reconstructed (U Sigma V^T):\n{U @ Sigma @ V.T}")
print(f"Original W:\n{W}")
print(f"Reconstruction error: {np.linalg.norm(U @ Sigma @ V.T - W):.2e}")
print(f"Singular values (descending): {sigmas}")
print(f"||x|| = {np.linalg.norm(x):.4f}")
print(f"||V^T x|| = {np.linalg.norm(V.T @ x):.4f}  (should equal ||x||)")
print(f"||U Sigma V^T x|| = {np.linalg.norm(U @ Sigma @ V.T @ x):.4f}")
print(f"||W x|| = {np.linalg.norm(W @ x):.4f}  (should equal previous)")
print(f"V orthogonal? V^T V =\n{V.T @ V}")
print(f"U orthogonal? U^T U =\n{U.T @ U}")

# Compute the four key vectors
Wx = W @ x
VTx = V.T @ x
SigmaVTx = Sigma @ VTx
USigmaVTx = U @ SigmaVTx  # equals W x by construction

print(f"W = \n{W}")
print(f"x = \n{x.reshape(-1, 1)}")
print(f"WtW = \n{WtW}")
print(f"V = \n{V}")
print(f"V.T = \n{V.T}")
print(f"VTx = \n{VTx.reshape(-1, 1)}")
print(f"eigenvecs = \n{eigvecs}")
print(f"eigenvals = \n{eigvals}")
print(f"sigmas = \n{sigmas}")
print(f"Sigma = \n{Sigma}")
print(f"SigmaVTx = \n{SigmaVTx}")
print(f"U = \n{U}")
print(f"USigmaVTx = \n{USigmaVTx}")
print(f"Wx = \n{Wx}")


# %% ---------------------------------------------------------------
# Plotting helpers
# ------------------------------------------------------------------
AXIS_LIM = 6  # canvas extends from -AXIS_LIM to +AXIS_LIM on each axis


def setup_canvas(ax, title):
    """Standard canvas: fixed horizontal/vertical axes, equal aspect."""
    ax.set_xlim(-AXIS_LIM, AXIS_LIM)
    ax.set_ylim(-AXIS_LIM, AXIS_LIM)
    ax.set_aspect("equal")
    ax.axhline(0, color="black", linewidth=0.8, zorder=2)
    ax.axvline(0, color="black", linewidth=0.8, zorder=2)
    ax.set_title(title, fontsize=11)


def standard_grid(ax, color="lightgray", alpha=0.7):
    """Light standard-basis gridlines."""
    for k in range(-AXIS_LIM, AXIS_LIM + 1):
        if k == 0:
            continue
        ax.axhline(k, color=color, linewidth=0.5, alpha=alpha, zorder=1)
        ax.axvline(k, color=color, linewidth=0.5, alpha=alpha, zorder=1)


def tilted_grid(ax, basis, color, alpha=0.5, n_lines=8):
    """
    Draw tilted axes + gridlines for a 2x2 orthonormal basis.

    basis: 2x2 array whose COLUMNS are the basis vectors b_1, b_2.
    The axes are drawn through the origin along b_1 and b_2.
    Gridlines are families of lines parallel to each axis at unit spacing
    in the basis direction.
    """
    b1 = basis[:, 0]
    b2 = basis[:, 1]

    # The two main axes (through origin)
    L = AXIS_LIM * 1.5  # extend beyond canvas so they reach the edges
    ax.plot(
        [-L * b1[0], L * b1[0]],
        [-L * b1[1], L * b1[1]],
        color=color,
        linewidth=1.5,
        zorder=2,
    )
    ax.plot(
        [-L * b2[0], L * b2[0]],
        [-L * b2[1], L * b2[1]],
        color=color,
        linewidth=1.5,
        zorder=2,
    )

    # Gridlines parallel to b_1, spaced along b_2 direction (and vice versa)
    for k in range(-n_lines, n_lines + 1):
        if k == 0:
            continue
        # Line parallel to b_1, offset by k*b_2
        offset = k * b2
        p1 = offset - L * b1
        p2 = offset + L * b1
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            color=color,
            linewidth=0.4,
            alpha=alpha,
            zorder=1,
        )
        # Line parallel to b_2, offset by k*b_1
        offset = k * b1
        p1 = offset - L * b2
        p2 = offset + L * b2
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            color=color,
            linewidth=0.4,
            alpha=alpha,
            zorder=1,
        )


def draw_vec(ax, vec, color, label, lw=2.5):
    """Draw an arrow from origin to vec with a label near the head."""
    ax.annotate(
        "",
        xy=(vec[0], vec[1]),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color=color, lw=lw, shrinkA=0, shrinkB=0),
        zorder=5,
    )
    # Label slightly past the arrowhead
    norm = np.linalg.norm(vec)
    if norm > 0:
        offset = 0.25 * vec / norm
        ax.text(
            vec[0] + offset[0],
            vec[1] + offset[1],
            label,
            color=color,
            fontsize=11,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=6,
        )


# %% ---------------------------------------------------------------
# Plot 1: x on the standard-basis canvas
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
setup_canvas(ax, "Plot 1: $x$ in the standard basis")
standard_grid(ax)
draw_vec(ax, x, color="C0", label=r"$x$")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot1_x.png"), dpi=120)
plt.close()


# %% ---------------------------------------------------------------
# Plot 2: x and Wx on the standard-basis canvas
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
setup_canvas(ax, "Plot 2: $x$ and $Wx$ (the black-box transformation)")
standard_grid(ax)
draw_vec(ax, x, color="C0", label=r"$x$")
draw_vec(ax, Wx, color="C3", label=r"$Wx$")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot2_Wx.png"), dpi=120)
plt.close()


# %% ---------------------------------------------------------------
# Plot 3: V tilted frame, with x and V^T x
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
setup_canvas(ax, r"Plot 3: $V$ frame (tilted), with $x$ and $V^T x$")
standard_grid(ax, color="lightgray", alpha=0.5)
tilted_grid(ax, V, color="steelblue", alpha=0.4)
draw_vec(ax, x, color="C0", label=r"$x$")
draw_vec(ax, VTx, color="C2", label=r"$V^T x$")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot3_VTx.png"), dpi=120)
plt.close()


# %% ---------------------------------------------------------------
# Plot 4: V and U tilted frames, with V^T x and Sigma V^T x
# Standard axes shown but no standard gridlines (per spec)
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
setup_canvas(ax, r"Plot 4: $V$ and $U$ frames, with $V^T x$ and $\Sigma V^T x$")
# NOTE: deliberately NOT calling standard_grid here
tilted_grid(ax, V, color="steelblue", alpha=0.4)
tilted_grid(ax, U, color="darkorange", alpha=0.4)
draw_vec(ax, VTx, color="C2", label=r"$V^T x$")
draw_vec(ax, SigmaVTx, color="C4", label=r"$\Sigma V^T x$")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot4_SigmaVTx.png"), dpi=120)
plt.close()


# %% ---------------------------------------------------------------
# Plot 5: Final composition U Sigma V^T x = W x
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
setup_canvas(ax, r"Plot 5: $U\Sigma V^T x = Wx$ (full reconstruction)")
standard_grid(ax, color="lightgray", alpha=0.5)
tilted_grid(ax, U, color="darkorange", alpha=0.4)
draw_vec(ax, SigmaVTx, color="C4", label=r"$\Sigma V^T x$")
draw_vec(ax, USigmaVTx, color="C3", label=r"$U\Sigma V^T x$")
# Sanity overlay: W x as a thin dashed arrow on top -- should coincide
ax.annotate(
    "",
    xy=(Wx[0], Wx[1]),
    xytext=(0, 0),
    arrowprops=dict(
        arrowstyle="->", color="black", lw=1.0, linestyle="dashed", shrinkA=0, shrinkB=0
    ),
    zorder=4,
)
ax.text(Wx[0] + 0.3, Wx[1] - 0.4, r"$Wx$ (dashed)", color="black", fontsize=9, zorder=6)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "plot5_full.png"), dpi=120)
plt.close()

print("\nAll 5 plots saved.")
