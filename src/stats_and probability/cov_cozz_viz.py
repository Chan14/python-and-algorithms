"""
Covariance & Correlation Visualization
---------------------------------------
A three-step visual journey from individual feature spread → covariance → correlation.

Convention (locked):
    D : data matrix, shape (N, d)  -- N examples, d features
    Each column D[:, j] is one feature.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# ---------------------------------------------------------------------------
# 1. Build a synthetic dataset with deliberately wired-in structure
# ---------------------------------------------------------------------------
def build_dataset(N=200, seed=42):
    """
    Construct D of shape (N, 4) with controlled covariance structure.

    Features:
        F0 = 'height_cm'     ~ N(170, 10^2)
        F1 = 'weight_kg'     strongly POSITIVELY correlated with F0
        F2 = 'screen_hours'  strongly NEGATIVELY correlated with F0
        F3 = 'lucky_number'  NEAR-ZERO correlation with everything (noise)

    Why these choices:
        - (F0, F1): tall people tend to weigh more  -> strong + correlation
        - (F0, F2): tall adults (vs kids) use screens less in this toy world -> strong - correlation
        - (F0, F3): lucky number has nothing to do with height -> ~0 correlation
        - F1 has much larger variance than F0 in absolute units -> lets us see
          how covariance is scale-dependent but correlation is not.
    """
    rng = np.random.default_rng(seed)

    # Latent "true" height signal, standardized
    z = rng.standard_normal(N)

    # F0: height in cm, mean 170, std 10
    F0 = 170 + 10 * z

    # F1: weight in kg, strongly + correlated with height, but with its own noise and scale
    #     true relationship: weight ≈ 0.9 * height_signal + noise, scaled to kg range
    F1 = 70 + 15 * (0.9 * z + 0.3 * rng.standard_normal(N))

    # F2: screen_hours, strongly - correlated with height
    F2 = 5 + 2 * (-0.85 * z + 0.4 * rng.standard_normal(N))

    # F3: lucky_number, independent noise
    F3 = 50 + 20 * rng.standard_normal(N)

    D = np.column_stack([F0, F1, F2, F3])
    feature_names = ["height_cm", "weight_kg", "screen_hours", "lucky_number"]
    return D, feature_names


# ---------------------------------------------------------------------------
# 2. Function 1: per-feature scatter (marginals)
# ---------------------------------------------------------------------------
def plot_feature_scatter(D, feature_names):
    """
    Plot each feature individually as a 1D strip scatter.

    Invariant: NO cross-feature info yet. Just mean and spread per feature.

    For each feature j we show:
        - the cloud of values (with small vertical jitter so points don't overlap)
        - a red vertical line at mu_j  (the sample mean)
        - a shaded band at mu_j +/- sigma_j  (one std dev)
    """
    N, d = D.shape
    fig, axes = plt.subplots(d, 1, figsize=(10, 2.0 * d))
    if d == 1:
        axes = [axes]

    rng = np.random.default_rng(0)  # fixed jitter for reproducibility

    for j in range(d):
        x = D[:, j]
        mu = x.mean()
        sigma = x.std(ddof=0)  # population std; we'll discuss ddof later if needed

        jitter = rng.uniform(-0.4, 0.4, size=N)
        axes[j].scatter(x, jitter, alpha=0.5, s=20, color="steelblue")

        # mean line
        axes[j].axvline(mu, color="red", linewidth=2, label=f"$\\mu$ = {mu:.2f}")
        # +/- 1 sigma band
        axes[j].axvspan(
            mu - sigma,
            mu + sigma,
            alpha=0.15,
            color="red",
            label=f"$\\mu \\pm \\sigma$  ($\\sigma$ = {sigma:.2f})",
        )

        axes[j].set_yticks([])
        axes[j].set_xlabel(feature_names[j])
        axes[j].set_title(
            f"Feature {j}: {feature_names[j]}    "
            f"$\\mu$={mu:.2f},  $\\sigma^2$={sigma**2:.2f}"
        )
        axes[j].legend(loc="upper right", fontsize=9)
        axes[j].grid(True, alpha=0.3)

    fig.suptitle("Step 1: Each feature alone (marginal view)", fontsize=13, y=1.00)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 3. Function 2: covariance plot for two features
# ---------------------------------------------------------------------------
def plot_covariance(D, j, k, feature_names):
    """
    Show covariance between features j and k as a quadrant-imbalance picture.

    Invariant: covariance is the average of (x_j - mu_j)(x_k - mu_k).
        - Quadrants Q1 (++) and Q3 (--) contribute POSITIVELY.
        - Quadrants Q2 (-+) and Q4 (+-) contribute NEGATIVELY.
        Covariance = (sum of contributions) / N.

    The plot makes that imbalance visible:
        - crosshair at (mu_j, mu_k) defines the four quadrants
        - quadrant background rectangles are drawn in DATA coordinates so they
          align exactly with the crosshair (no bleed-through at the mean)
        - points are colored green if they push covariance UP, red if DOWN
        - sigma reference lines at mu +/- 1, 2, 3 sigma on each axis (marginal
          facts about each feature individually; no joint-shape claim)
        - title shows the numerical Cov(X_j, X_k)
    """
    from matplotlib.patches import Rectangle, Patch

    xj = D[:, j]
    xk = D[:, k]
    mu_j = xj.mean()
    mu_k = xk.mean()
    sig_j = xj.std(ddof=0)
    sig_k = xk.std(ddof=0)

    # centered values
    cj = xj - mu_j
    ck = xk - mu_k

    # per-point contribution to covariance
    contrib = cj * ck
    cov = contrib.mean()  # this IS the covariance (population form, divide by N)

    # color by sign of contribution
    colors = np.where(contrib >= 0, "green", "red")

    fig, ax = plt.subplots(figsize=(8, 7))

    # axis limits: pad enough to comfortably show +/- 3 sigma reference lines
    xmin = min(xj.min(), mu_j - 3.2 * sig_j)
    xmax = max(xj.max(), mu_j + 3.2 * sig_j)
    ymin = min(xk.min(), mu_k - 3.2 * sig_k)
    ymax = max(xk.max(), mu_k + 3.2 * sig_k)
    xpad = 0.03 * (xmax - xmin)
    ypad = 0.03 * (ymax - ymin)
    xlim = (xmin - xpad, xmax + xpad)
    ylim = (ymin - ypad, ymax + ypad)

    # ----- quadrant shading in DATA coordinates -----
    # Each rectangle's corner sits exactly at (mu_j, mu_k), so the four
    # quadrants meet precisely at the crosshair with no axes-coord drift.
    quadrants = [
        # (x0, y0, width, height, color, label)
        (mu_j, mu_k, xlim[1] - mu_j, ylim[1] - mu_k, "green"),  # Q1: ++
        (xlim[0], mu_k, mu_j - xlim[0], ylim[1] - mu_k, "red"),  # Q2: -+
        (xlim[0], ylim[0], mu_j - xlim[0], mu_k - ylim[0], "green"),  # Q3: --
        (mu_j, ylim[0], xlim[1] - mu_j, mu_k - ylim[0], "red"),  # Q4: +-
    ]
    for x0, y0, w, h, c in quadrants:
        ax.add_patch(
            Rectangle(
                (x0, y0), w, h, facecolor=c, alpha=0.05, edgecolor="none", zorder=0
            )
        )

    # ----- sigma reference lines (marginal, one feature at a time) -----
    # Vertical lines at mu_j +/- n * sigma_j  (a fact about feature j only)
    # Horizontal lines at mu_k +/- n * sigma_k  (a fact about feature k only)
    # No inline labels: the axis tick labels themselves (set below) sit
    # exactly at these positions and carry the meaning.
    sigma_styles = {
        1: {"ls": "-", "lw": 1.2, "alpha": 0.55},  # 1-sigma: solid
        2: {"ls": "--", "lw": 1.0, "alpha": 0.40},  # 2-sigma: dashed
        3: {"ls": ":", "lw": 1.0, "alpha": 0.30},  # 3-sigma: dotted
    }
    SIGMA_COLOR = "gray"
    for n, style in sigma_styles.items():
        for sign in (-1, +1):
            ax.axvline(
                mu_j + sign * n * sig_j,
                color=SIGMA_COLOR,
                linestyle=style["ls"],
                linewidth=style["lw"],
                alpha=style["alpha"],
                zorder=1,
            )
            ax.axhline(
                mu_k + sign * n * sig_k,
                color=SIGMA_COLOR,
                linestyle=style["ls"],
                linewidth=style["lw"],
                alpha=style["alpha"],
                zorder=1,
            )

    # ----- ticks at mu and mu +/- n*sigma on both axes -----
    # The tick POSITION is the sigma reference; the tick LABEL is the actual
    # data value at that position.  Mean tick is bolded so it reads as "anchor".
    x_tick_positions = [mu_j + n * sig_j for n in range(-3, 4)]
    y_tick_positions = [mu_k + n * sig_k for n in range(-3, 4)]
    ax.set_xticks(x_tick_positions)
    ax.set_yticks(y_tick_positions)
    ax.set_xticklabels([f"{v:.2f}" for v in x_tick_positions])
    ax.set_yticklabels([f"{v:.2f}" for v in y_tick_positions])
    # bold the center tick (index 3 = the mean) so the anchor stands out
    ax.get_xticklabels()[3].set_fontweight("bold")
    ax.get_yticklabels()[3].set_fontweight("bold")

    # ----- the data -----
    ax.scatter(
        xj, xk, c=colors, alpha=0.6, s=25, edgecolors="black", linewidths=0.3, zorder=3
    )

    # ----- crosshair at the joint mean -----
    ax.axvline(mu_j, color="black", linewidth=1.4, linestyle="--", alpha=0.8, zorder=2)
    ax.axhline(mu_k, color="black", linewidth=1.4, linestyle="--", alpha=0.8, zorder=2)

    # mean point marker
    ax.plot(
        mu_j,
        mu_k,
        "k*",
        markersize=15,
        zorder=4,
        label=f"$(\\mu_j, \\mu_k)$ = ({mu_j:.2f}, {mu_k:.2f})",
    )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel(f"{feature_names[j]}  (feature {j})    " f"$\\sigma_j$ = {sig_j:.2f}")
    ax.set_ylabel(f"{feature_names[k]}  (feature {k})    " f"$\\sigma_k$ = {sig_k:.2f}")
    ax.set_title(
        f"Step 2: Covariance view\n"
        f"Cov({feature_names[j]}, {feature_names[k]}) = {cov:.3f}    "
        f"(units: {feature_names[j]} $\\times$ {feature_names[k]})",
        fontsize=11,
    )
    ax.legend(loc="best", fontsize=9)
    ax.grid(False)  # off: the sigma lines are our reference grid now

    # second legend explaining color coding
    extra = [
        Patch(facecolor="green", alpha=0.4, label="pushes Cov UP  (++ or --)"),
        Patch(facecolor="red", alpha=0.4, label="pushes Cov DOWN (+- or -+)"),
    ]
    leg2 = ax.legend(
        handles=extra, loc="lower right", fontsize=9, title="per-point contribution"
    )
    ax.add_artist(leg2)

    fig.tight_layout()
    return fig, cov


# ---------------------------------------------------------------------------
# 4. Function 3: correlation plot for two features
# ---------------------------------------------------------------------------
def plot_correlation(D, j, k, feature_names):
    """
    Show correlation between features j and k by STANDARDIZING both features.

    Invariant: correlation = covariance of the standardized data.
        After we replace x_j with (x_j - mu_j)/sigma_j (and same for k):
            - both axes have mean 0 and variance 1
            - axes are dimensionless
            - the cov of these standardized features IS rho_{jk}, bounded in [-1, 1]

    The plot shows:
        - standardized scatter
        - crosshair at origin
        - unit circle overlay (the "1 std dev" reference)
        - best-fit line through origin with slope = rho_{jk}
        - title shows rho_{jk}
    """
    xj = D[:, j]
    xk = D[:, k]
    mu_j, mu_k = xj.mean(), xk.mean()
    sig_j, sig_k = xj.std(ddof=0), xk.std(ddof=0)

    # standardize
    zj = (xj - mu_j) / sig_j
    zk = (xk - mu_k) / sig_k

    # correlation = mean of product of standardized values
    rho = (zj * zk).mean()

    fig, ax = plt.subplots(figsize=(8, 7))

    # quadrant shading using same color convention as before
    ax.axvspan(0, 5, ymin=0.5, ymax=1.0, alpha=0.05, color="green")
    ax.axvspan(-5, 0, ymin=0.0, ymax=0.5, alpha=0.05, color="green")
    ax.axvspan(0, 5, ymin=0.0, ymax=0.5, alpha=0.05, color="red")
    ax.axvspan(-5, 0, ymin=0.5, ymax=1.0, alpha=0.05, color="red")

    # scatter
    contrib = zj * zk
    colors = np.where(contrib >= 0, "green", "red")
    ax.scatter(zj, zk, c=colors, alpha=0.6, s=25, edgecolors="black", linewidths=0.3)

    # crosshair at origin (standardized data has mean 0)
    ax.axvline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
    ax.axhline(0, color="black", linewidth=1.2, linestyle="--", alpha=0.7)

    # unit circle: visual marker for "1 std dev in each direction"
    circle = Circle(
        (0, 0),
        1.0,
        fill=False,
        color="blue",
        linewidth=2,
        linestyle="-",
        label="unit circle (1 std dev)",
    )
    ax.add_patch(circle)

    # best-fit line through origin with slope = rho
    # (this is the regression line of standardized data)
    x_line = np.linspace(-4, 4, 100)
    ax.plot(
        x_line,
        rho * x_line,
        color="purple",
        linewidth=2,
        label=f"slope = $\\rho$ = {rho:.3f}",
    )

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")  # CRITICAL: equal aspect so the geometry is honest
    ax.set_xlabel(f"standardized {feature_names[j]}: $(x_j - \\mu_j)/\\sigma_j$")
    ax.set_ylabel(f"standardized {feature_names[k]}: $(x_k - \\mu_k)/\\sigma_k$")
    ax.set_title(
        f"Step 3: Correlation view (standardized, dimensionless)\n"
        f"$\\rho$({feature_names[j]}, {feature_names[k]}) = {rho:.3f}   "
        f"(bounded in [-1, 1])",
        fontsize=11,
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig, rho


# ---------------------------------------------------------------------------
# 5. Summary statistics: means and standard deviations per feature
# ---------------------------------------------------------------------------
def print_feature_summary(D, feature_names):
    """
    Print a per-feature table of mean, variance, and standard deviation.

    Invariant: this is the MARGINAL summary — no cross-feature info yet.
    Each row reports what you'd see if you looked at one column of D in isolation.
    """
    N, d = D.shape
    print("=" * 72)
    print(f"Per-feature summary  (N = {N} examples, d = {d} features)")
    print("=" * 72)
    print(
        f"{'idx':<5}{'feature':<18}{'mean (mu)':>14}{'var (sigma^2)':>18}"
        f"{'std (sigma)':>15}"
    )
    print("-" * 72)
    for j in range(d):
        x = D[:, j]
        mu = x.mean()
        var = x.var(ddof=0)  # population variance: divide by N
        sigma = np.sqrt(var)
        print(f"{j:<5}{feature_names[j]:<18}{mu:>14.4f}{var:>18.4f}{sigma:>15.4f}")
    print()


# ---------------------------------------------------------------------------
# 6. Covariance matrix  Sigma  of shape (d, d)
# ---------------------------------------------------------------------------
def covariance_matrix(D):
    """
    Build the d x d covariance matrix Sigma where
        Sigma[j, k] = Cov(X_j, X_k) = (1/N) * sum_i (x_ij - mu_j)(x_ik - mu_k)

    Two computations, side by side, both returning the same matrix:
        - Sigma_loop : explicit double loop, one cell at a time
        - Sigma_vec  : vectorized form  Sigma = (1/N) * Dc^T @ Dc
                       where Dc is the column-centered data matrix

    We return Sigma_vec but assert they agree, to make the equivalence concrete.
    """
    N, d = D.shape
    mu = D.mean(axis=0)  # shape (d,) -- one mean per feature
    Dc = D - mu  # broadcast subtraction; Dc has shape (N, d)

    # -- explicit loop version (pedagogical) --
    Sigma_loop = np.zeros((d, d))
    for j in range(d):
        for k in range(d):
            Sigma_loop[j, k] = (Dc[:, j] * Dc[:, k]).mean()

    # -- vectorized version (the matrix form we will study next) --
    Sigma_vec = (Dc.T @ Dc) / N

    # sanity check: the two ways must agree to floating-point precision
    assert np.allclose(
        Sigma_loop, Sigma_vec
    ), "Loop and vectorized covariance disagree -- something is wrong!"

    return Sigma_vec


# ---------------------------------------------------------------------------
# 7. Correlation matrix  R  of shape (d, d)
# ---------------------------------------------------------------------------
def correlation_matrix(D):
    """
    Build the d x d correlation matrix R where
        R[j, k] = rho_{jk} = Cov(X_j, X_k) / (sigma_j * sigma_k)

    Equivalently: R is the covariance matrix of the STANDARDIZED data.
        Z[:, j] = (D[:, j] - mu_j) / sigma_j
        R = (1/N) * Z^T @ Z

    Properties to notice when you print it:
        - diagonal is all 1s  (a feature is perfectly correlated with itself)
        - symmetric:  R[j, k] == R[k, j]
        - every entry lies in [-1, 1]
    """
    N, d = D.shape
    mu = D.mean(axis=0)
    sigma = D.std(axis=0, ddof=0)
    Z = (D - mu) / sigma  # standardized data, shape (N, d)
    R = (Z.T @ Z) / N
    return R


def print_matrix(M, feature_names, title):
    """
    Pretty-print a square matrix with feature names as row/column headers.
    """
    d = M.shape[0]
    print("=" * 72)
    print(title)
    print("=" * 72)
    # header row
    header = " " * 16 + "".join(f"{name:>14}" for name in feature_names)
    print(header)
    print("-" * len(header))
    for j in range(d):
        row = f"{feature_names[j]:<16}" + "".join(f"{M[j, k]:>14.4f}" for k in range(d))
        print(row)
    print()


# ---------------------------------------------------------------------------
# 8. Run the demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os

    # Save plots next to this script, regardless of where it is run from.
    OUT_DIR = os.path.dirname(os.path.abspath(__file__))

    np.set_printoptions(precision=4, suppress=True)

    D, names = build_dataset(N=200, seed=42)

    print(
        f"Data matrix D shape: {D.shape}   (N={D.shape[0]} examples, d={D.shape[1]} features)"
    )
    print(f"Features: {names}\n")

    # ---- per-feature summary (means, variances, stds) ----
    print_feature_summary(D, names)

    # ---- covariance matrix ----
    Sigma = covariance_matrix(D)
    print_matrix(
        Sigma,
        names,
        "Covariance matrix  Sigma = (1/N) * Dc^T @ Dc   "
        "(units: feature_j * feature_k)",
    )

    # ---- correlation matrix ----
    R = correlation_matrix(D)
    print_matrix(
        R,
        names,
        "Correlation matrix  R   "
        "(dimensionless, all entries in [-1, 1], diagonal = 1)",
    )

    # ---- Step 1: marginals plot ----
    fig1 = plot_feature_scatter(D, names)
    fig1.savefig(
        os.path.join(OUT_DIR, "step1_marginals.png"), dpi=110, bbox_inches="tight"
    )
    plt.close(fig1)

    # ---- Steps 2 & 3: three illustrative pairs ----
    pairs = [
        (0, 1, "A_strong_positive"),
        (0, 2, "B_strong_negative"),
        (0, 3, "C_near_zero"),
    ]

    print("=" * 72)
    print("Per-pair check  (these numbers must match Sigma and R above)")
    print("=" * 72)
    print(f"{'pair':<32}{'Cov':>12}{'rho':>12}")
    print("-" * 56)
    for j, k, tag in pairs:
        fig_cov, cov_val = plot_covariance(D, j, k, names)
        fig_cov.savefig(
            os.path.join(OUT_DIR, f"step2_cov_{tag}.png"), dpi=110, bbox_inches="tight"
        )
        plt.close(fig_cov)

        fig_corr, rho_val = plot_correlation(D, j, k, names)
        fig_corr.savefig(
            os.path.join(OUT_DIR, f"step3_corr_{tag}.png"), dpi=110, bbox_inches="tight"
        )
        plt.close(fig_corr)

        pair_label = f"{names[j]} vs {names[k]}"
        print(f"{pair_label:<32}{cov_val:>12.4f}{rho_val:>12.4f}")

    print(f"\nPlots saved to: {OUT_DIR}")
