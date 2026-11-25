import numpy as np

from pyalgos.stats.covariance_correlation import (
    build_dataset,
    correlation_matrix,
    covariance_matrix,
)


def test_covariance_matches_numpy_population_cov():
    D, _ = build_dataset(N=200, seed=42)
    # Our Sigma uses 1/N (population), so compare with bias=True.
    np.testing.assert_allclose(covariance_matrix(D), np.cov(D, rowvar=False, bias=True))


def test_correlation_matches_numpy_and_invariants():
    D, _ = build_dataset(N=200, seed=42)
    R = correlation_matrix(D)
    np.testing.assert_allclose(R, np.corrcoef(D, rowvar=False))
    np.testing.assert_allclose(np.diag(R), 1.0)
    np.testing.assert_allclose(R, R.T)
    assert np.all(np.abs(R) <= 1 + 1e-12)


def test_correlation_is_scale_invariant_but_covariance_is_not():
    D, _ = build_dataset(N=200, seed=1)
    scaled = D * np.array([100.0, 1.0, 1.0, 1.0])  # e.g. metres -> centimetres
    np.testing.assert_allclose(correlation_matrix(scaled), correlation_matrix(D))
    assert not np.allclose(covariance_matrix(scaled), covariance_matrix(D))
