import pytest

from pyalgos.algorithms.two_pointers.valid_subsequence import (
    is_valid_subsequence,
    is_valid_subsequence_v1,
)


@pytest.mark.parametrize("fn", [is_valid_subsequence_v1, is_valid_subsequence])
@pytest.mark.parametrize(
    "array, sequence, expected",
    [
        ([5, 1, 22, 25, 6, -1, 8, 10], [1, 6, -1, 10], True),
        ([1, 2, 3], [], True),
        ([], [1], False),
        ([1, 1, 1, 1], [1, 1], True),
        ([1, 2, 3], [3, 2], False),
    ],
)
def test_is_valid_subsequence(fn, array, sequence, expected):
    assert fn(array, sequence) is expected
