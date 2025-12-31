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

# The Next Level: "Skipping" at the Source
# There is one tiny refactor that separates a "good" solution from a "robust" one. Instead of checking c[-1] every time, some engineers prefer to "drain" duplicates from the source arrays using a nested while loop or by jumping the pointers.

# Why? Because it keeps the logic of "finding a match" separate from the logic of "handling output."

# The "skip logic" is a subtle but powerful shift in how you manage your pointers. In your previous version, you used the output (c[-1]) to decide if you should add a number. With skip logic, you use the input to ensure you only ever consider a unique number once.

# The Refined Invariant
# To support skipping, we tighten the invariant:

# At the start of each iteration, a_idx and b_idx point to the first occurrence of a new value in their respective arrays that hasn't been processed yet.

# The "Skip" Implementation
# Instead of checking the output array, we advance our pointers past all identical values immediately after we find a match.


def intersect_with_skipping(A, B):
    a_idx = 0
    b_idx = 0
    c = []
    # Invariant : At the start of each iteration, a_idx and b_idx point to the first occurrence of a new value in their respective arrays that hasn't been processed yet.
    while a_idx < len(A) and b_idx < len(B):
        if A[a_idx] < B[b_idx]:
            a_idx += 1
        elif A[a_idx] > B[b_idx]:
            b_idx += 1
        else:
            # we found a match
            current_val = A[a_idx]
            c.append(current_val)

            while a_idx < len(A) and A[a_idx] == current_val:
                a_idx += 1
            while b_idx < len(B) and B[b_idx] == current_val:
                b_idx += 1
    return c


# Why this is a "Level Up"
# Feature               c[-1] Approach                          The "Skip" Approach
# Responsibility        The Output handles uniqueness.          The Pointers handle uniqueness.
# Clarity               Very Pythonic and concise.              More "Low-level" and explicit.
# Separation            Logic is mixed (matching + checking).   Logic is separate (matching, then advancing).
# Edge Cases            Relies on c not being empty.            Relies only on array boundaries.

print(intersect_with_skipping([1, 3, 3, 5, 5, 7, 9], [1, 3, 5, 7, 9]))
print(intersect_with_skipping([5, 5, 9], [1, 3, 5, 7, 9]))
print(intersect_with_skipping([1, 3, 5, 7, 9], [9]))
print(intersect_with_skipping([], [9]))
print(intersect_with_skipping([], []))

# In an interview, the "Skip" approach is often preferred because it shows you can control your data stream at the source. If c was a write-only stream (like a network socket or a file) where you couldn't check c[-1], your original logic would break. The "Skip" logic would still work perfectly.
