import pytest

from pyalgos.algorithms.two_pointers.merge_and_intersect import (
    intersect,
    intersect_with_skipping,
    merge_arrays,
)


@pytest.mark.parametrize(
    "a, b",
    [([], []), ([], [1, 3]), ([2, 4], []), ([1, 3, 5], [2, 4, 6, 8]), ([1, 1, 2], [1, 2, 2])],
)
def test_merge_arrays_matches_sorted(a, b):
    assert merge_arrays(a, b) == sorted(a + b)


@pytest.mark.parametrize("fn", [intersect, intersect_with_skipping])
@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([], [], []),
        ([], [9], []),
        ([1, 3, 3, 5, 5, 7, 9], [1, 3, 5, 7, 9], [1, 3, 5, 7, 9]),
        ([5, 5, 9], [1, 3, 5, 7, 9], [5, 9]),
        ([1, 2], [3, 4], []),
    ],
)
def test_intersect_unique_sorted(fn, a, b, expected):
    assert fn(a, b) == expected
