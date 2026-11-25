from pyalgos.algorithms.two_pointers.merge_sorted_lists import merge


def test_merge_empty_lists():
    assert merge([], []) == []


def test_merge_one_list_empty():
    assert merge([], [5, 6]) == [5, 6]
    assert merge([5, 6], []) == [5, 6]


def test_merge_full_lists():
    assert merge([1, 4, 9], [2, 3, 10, 17]) == [1, 2, 3, 4, 9, 10, 17]
    assert merge([1, 4, 9], [2, 3, 10, 17, 17]) == [1, 2, 3, 4, 9, 10, 17, 17]
    assert merge([2, 3, 10, 17], [1, 4, 9]) == [1, 2, 3, 4, 9, 10, 17]
    assert merge([2, 3, 10, 17, 17], [1, 4, 9]) == [1, 2, 3, 4, 9, 10, 17, 17]


def test_input_lists_unchanged():
    list1, list2 = [], []
    merge(list1, list2).append(0)
    assert list1 == [] and list2 == []
    list1, list2 = [1, 2], []  # list2 reassigned for readbility
    merge(list1, list2).append(0)
    assert list1 == [1, 2] and list2 == []
    list1, list2 = [], [1, 2]  # list2 reassigned for readbility
    merge(list1, list2).append(0)
    assert list1 == [] and list2 == [1, 2]
