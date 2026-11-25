import random

from pyalgos.algorithms.monotonic_deque.shortest_subarray_at_least_k import (
    shortest_subarray_at_least_k,
)


def brute_force(nums, k):
    lengths = [
        j - i
        for i in range(len(nums))
        for j in range(i + 1, len(nums) + 1)
        if sum(nums[i:j]) >= k
    ]
    return min(lengths, default=-1)


def test_example():
    assert shortest_subarray_at_least_k([2, -1, 2, 1], 3) == 2


def test_no_valid_subarray():
    assert shortest_subarray_at_least_k([-1, -2], 1) == -1


def test_matches_brute_force_with_negatives():
    # Random arrays WITH negatives: exactly where plain sliding window breaks.
    rng = random.Random(0)
    for _ in range(500):
        nums = [rng.randint(-6, 9) for _ in range(rng.randint(1, 12))]
        k = rng.randint(1, 20)
        assert shortest_subarray_at_least_k(nums, k) == brute_force(nums, k)
