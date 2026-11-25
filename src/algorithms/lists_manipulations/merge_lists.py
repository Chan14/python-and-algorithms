def merge(a: list[float], b: list[float]) -> list[float]:
    """Return a new sorted list containing all elements of a and b.

    Assumes a and b are each already in non-decreasing order.
    Does not modify a or b.
    """
    id1, id2, hi1, hi2 = 0, 0, len(a), len(b)
    result = []
    # Invariants: at the top of each iteration,
    # 1. result contains exactly the elements of a[:id1] and b[:id2].
    # 2. result is sorted in non-decreasing order.
    # 3. every element of result <= every element of a[id1:] and of b[id2:].
    while (id1 < hi1) and (id2 < hi2):
        if a[id1] <= b[id2]:
            result.append(a[id1])
            id1 += 1
        else:
            result.append(b[id2])
            id2 += 1
    result += a[id1:]  # += in place extend. result.extend(a[id1:]) is in place too.
    result += b[id2:]
    return result
