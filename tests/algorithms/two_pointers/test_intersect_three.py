from pyalgos.algorithms.two_pointers.intersect_three import intersect_three


def test_basic():
    a = [1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9]
    assert intersect_three(a, [2, 3, 4, 5], [4, 5, 5, 6, 7]) == [4, 5]


def test_two_way_match_with_third_smaller():
    # A=5, B=5, C=2 must advance C without any special "two-way match" case.
    assert intersect_three([5], [5], [2, 5]) == [5]


def test_any_empty_gives_empty():
    assert intersect_three([], [1], [1]) == []
    assert intersect_three([1], [1], []) == []
