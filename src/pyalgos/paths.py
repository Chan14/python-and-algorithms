"""Repo-relative paths, so scripts write to the same place whatever the cwd.

Assumption (invariant): pyalgos is installed in editable mode from a source
checkout (`pip install -e .`), so this file lives at
<repo>/src/pyalgos/paths.py. If that does not hold, we fail loudly instead of
silently writing figures somewhere unexpected.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def figures_dir(*parts: str) -> Path:
    """Return <repo>/figures/<parts...>, creating it if needed.

    Example: figures_dir("stats", "covariance") -> <repo>/figures/stats/covariance
    """
    if not (REPO_ROOT / "pyproject.toml").is_file():
        raise RuntimeError(
            f"Expected a source checkout at {REPO_ROOT}; "
            "install with `pip install -e .` from the repo root."
        )
    out = REPO_ROOT.joinpath("figures", *parts)
    out.mkdir(parents=True, exist_ok=True)
    return out
