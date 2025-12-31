# Problem: Merge Two Sorted Arrays
#     We are given two arrays A and B.
#     Explicit assumptions (contract of the function)
#     1️⃣ Input validity
#         A and B are arrays (lists) of integers
#         Elements may be negative, zero, or positive
#         Duplicates are allowed
#     2️⃣ Sortedness
#         A is sorted in non-decreasing order
#         B is sorted in non-decreasing order
#         This is a hard assumption.
#         If violated, correctness is not guaranteed — but that’s outside the scope of this problem.
#     3️⃣ Length / emptiness
#         A may be empty
#         B may be empty
#         Both may be empty
#         These are not special cases — they must fall out naturally from the logic + invariant.

#     Examples:
#         A = [], B = [1, 3, 5] → result is [1, 3, 5]
#         A = [], B = [] → result is []
#     4️⃣ Memory model
#         We are allowed to allocate a new output array C
#         We are not required to merge in-place
#         Time complexity target: O(len(A) + len(B))
#         Extra space: O(len(A) + len(B))
#     5️⃣ Comparison semantics
#         Standard integer comparison (<, <=)
#      Stability:
#         If A[a_idx] == B[b_idx], either order is acceptable
#         (If we wanted stability across arrays, we’d specify it — but we didn’t)
#     6️⃣ Failure conditions
#         None, given the assumptions above
#         This is a total function:
#     For every valid input satisfying the assumptions, the algorithm must terminate and produce a result
#     Failures like:
#         index errors
#         infinite loops
#         missing elements
#     are implementation bugs, not logical edge cases.
#     What the algorithm must guarantee
#     Output array C:
#         contains all elements of A and B
#         contains no extra elements
#         is sorted in non-decreasing order


def merge_arrays(A, B):
    """
    Return a new array containing all elements of A and B in non-decreasing order

    Args:
        A : an array sorted in non decreasing order
        B : an array sorted in non decreasing order
    """
    a_idx = 0
    b_idx = 0
    c_idx = 0
    c = [0] * (len(A) + len(B))
    # Invariant: c[0:c_idx] contains the smallest elements from
    # A[0:a_idx] ∪ B[0:b_idx] in sorted order
    while a_idx < len(A) and b_idx < len(B):
        if A[a_idx] <= B[b_idx]:
            c[c_idx] = A[a_idx]
            a_idx += 1
        else:
            c[c_idx] = B[b_idx]
            b_idx += 1
        c_idx += 1
    if a_idx < len(A):
        c[c_idx:] = A[a_idx:]
    if b_idx < len(B):
        c[c_idx:] = B[b_idx:]
    return c


print(merge_arrays([1, 3, 5, 7, 9], [2, 4, 6, 8, 10, 12, 14]))
print(merge_arrays([], [2, 4, 6, 8, 10, 12, 14]))
print(merge_arrays([1, 3, 5, 7, 9], []))
print(merge_arrays([], []))

# Problem — read carefully
# Intersection of Two Sorted Arrays (Invariant-first)
# You are given two sorted arrays, A and B.
# Your task: produce a new array c containing only the unique elements that appear in both arrays, in sorted order.

# Constraints:
# Arrays may be different lengths
# Duplicates may exist in A and/or B
# Output must not have duplicates
# No flags, no special cases — the invariant must capture correctness


# We are still not coding.
# Summary —
# Pointers / state:
#   a_idx: next element in A to consume
#   b_idx: next element in B to consume
# c: c contains all unique elements found so far that are in both A[0:a_idx] and B[0:b_idx], in sorted order.
# Invariant:
#   c contains all unique elements found so far that are in both A[0:a_idx] and B[0:b_idx], in sorted order.
# Completion / success:
#   Loop continues while both arrays have unconsumed elements.
#   Loop ends when one array is exhausted → intersection is complete.
# Failure: None — the absence of common elements is naturally represented by C being empty.
def intersect(A, B):
    """
    Return a new array containing all intersecting, unique elements of A and B in non-decreasing order

    Args:
        A : an array sorted in non decreasing order
        B : an array sorted in non decreasing order
    """
    a_idx = 0
    b_idx = 0
    c = []
    # Invariant: c contains all unique elements found so far that are in both A[0:a_idx] and B[0:b_idx], in sorted order.
    while a_idx < len(A) and b_idx < len(B):
        if A[a_idx] < B[b_idx]:
            a_idx += 1
        elif A[a_idx] > B[b_idx]:
            b_idx += 1
        else:
            if not c or c[-1] != A[a_idx]:
                c.append(A[a_idx])
            a_idx += 1
            b_idx += 1
    return c


print(intersect([1, 3, 3, 5, 5, 7, 9], [1, 3, 5, 7, 9]))
print(intersect([5, 5, 9], [1, 3, 5, 7, 9]))
print(intersect([1, 3, 5, 7, 9], [9]))
print(intersect([], [9]))
print(intersect([], []))
