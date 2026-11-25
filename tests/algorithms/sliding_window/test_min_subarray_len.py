import random

from pyalgos.algorithms.sliding_window.min_subarray_len import (
    min_subarray,
    min_subarray_len,
)


def brute_force_len(K, A):
    lengths = [
        j - i
        for i in range(len(A))
        for j in range(i + 1, len(A) + 1)
        if sum(A[i:j]) >= K
    ]
    return min(lengths, default=0)


def test_example():
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_subarray(7, [2, 3, 1, 2, 4, 3]) == [4, 3]


def test_no_valid_window():
    assert min_subarray_len(100, [1, 2, 3]) == 0
    assert min_subarray(100, [1, 2, 3]) == []  # used to raise IndexError
    assert min_subarray(1, []) == []


def test_matches_brute_force_on_random_positive_arrays():
    rng = random.Random(0)
    for _ in range(300):
        A = [rng.randint(1, 9) for _ in range(rng.randint(0, 12))]
        K = rng.randint(1, 40)
        expected = brute_force_len(K, A)
        assert min_subarray_len(K, A) == expected
        window = min_subarray(K, A)
        assert len(window) == expected
        assert not window or sum(window) >= K
