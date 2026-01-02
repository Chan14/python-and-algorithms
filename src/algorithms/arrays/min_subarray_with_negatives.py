"""
Problem: Shortest Subarray with Sum at Least K

Given an array of integers nums (which may contain both positive and negative
values) and an integer k, find the length of the shortest non-empty contiguous
subarray whose sum is greater than or equal to k.

If no such subarray exists, return -1.

Constraints / Notes:
- The array may contain negative numbers.
- The solution must correctly handle cases where classical sliding window
  techniques fail due to the presence of negative values.
- The goal is to achieve an efficient solution with linear time complexity.

Example:
Input:
    nums = [2, -1, 2, 1]
    k = 3

Output:
    2

Explanation:
    The subarray [2, 1] has sum = 3 and length = 2, which is the shortest
    contiguous subarray with sum >= k.
"""

from typing import List
from collections import deque


def shortest_subarray_at_least_k(nums: List[int], k: int) -> int:
    """
    Returns the length of the shortest non-empty subarray
    with sum >= k. If no such subarray exists, return -1.
    """
    # Initialize prefix sums array
    # Future optimization if space is a constraint - we need prefix sums only for the candidate starts so we can populate it on the go and keep it aligned with starts deque.
    P = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        P[i + 1] = P[i] + nums[i]
    # Initialize deque and cached results
    starts = deque()
    best_len = float("inf")
    # best_window = [] # left and right indices
    for j in range(len(P)):
        while starts and P[j] - P[starts[0]] >= k:
            best_len = min(best_len, j - starts.popleft())
            # left = starts.popleft()
            # window_len = j - left
            # if window_len < best_len:
            #     best_len = window_len
            #     best_window = [left, j]
        while starts and P[j] <= P[starts[-1]]:
            starts.pop()
        starts.append(j)
    # return nums[best_window[0]:best_window[1]] # No +1 correction needed. These are prefix sum indices.
    return -1 if best_len == float("inf") else best_len


print(shortest_subarray_at_least_k([2, 4, -3, 4, 2, 6, 1, 2], 6))
"""
Why Sliding Window Fails
-----------------------
A classical sliding window approach relies on the property that removing elements
from the left monotonically decreases the window sum. This property holds only
when all elements are non-negative.

When negative numbers are allowed, shrinking the window from the left may
increase the sum, causing valid candidate subarrays to be skipped entirely.
Therefore, sliding window is no longer dominance-complete and cannot guarantee
correctness.

To address this, we switch from maintaining a window to maintaining a set of
non-dominated prefix-sum states.
"""


"""
Key Idea
--------
Let P be the prefix sum array where:
    P[0] = 0
    P[i] = nums[0] + nums[1] + ... + nums[i-1]

The sum of subarray nums[i : j] is:
    P[j] - P[i]

We want to find the minimum (j - i) such that:
    P[j] - P[i] >= k
"""


"""
Deque Invariant
---------------
At the start of each iteration with index j, the deque `starts` satisfies:

1. All indices in `starts` are strictly increasing.
2. Their corresponding prefix sums are strictly increasing:
       P[starts[0]] < P[starts[1]] < ... < P[starts[-1]]
3. Each index i in `starts` is a viable subarray start for some future end index
   t >= j.
4. No index in `starts` is dominated by another:
       An index i1 dominates i2 if i1 < i2 and P[i1] <= P[i2].
5. Every subarray starting at an index less than starts[0] and ending at any
   index less than j has already been considered and cannot produce a shorter
   valid answer.

This invariant ensures correctness and allows safe pruning.
"""


"""
Dominance and Pruning Logic
---------------------------
1. Front Pruning (Exhaustion):
   While P[j] - P[starts[0]] >= k, we have found the shortest possible subarray
   ending at j for that start index. Since future j' > j would only increase the
   length, that start index is exhausted and can be safely removed.

2. Back Pruning (Dominance):
   While P[j] <= P[starts[-1]], the index at the back is dominated by j.
   The newer index j is always at least as good a start (larger or equal sum,
   later position → potentially shorter subarrays), so the dominated index is
   removed.

Together, these rules maintain a monotonic, non-dominated frontier of candidate
starts.
"""


"""
Correctness Intuition
---------------------
- The deque maintains all and only non-dominated prefix-sum states.
- Every valid subarray is considered exactly once when its start index is popped
  from the front.
- No optimal solution is skipped because dominated or exhausted starts can never
  produce a shorter valid subarray in the future.
"""


"""
Complexity Analysis
-------------------
Time Complexity: O(n)
- Each index is added to the deque once.
- Each index is removed from the deque at most once from the front and once from
  the back.
- Total deque operations are linear (amortized).

Space Complexity: O(n)
- Prefix sum array requires O(n) space.
- Deque may contain up to O(n) indices in the worst case.

The algorithm is optimal for this problem.
"""


"""
Invariant :
-----------
    At iteration j, starts is a deque of indices i < j such that:
    Prefix sums P[i] are strictly increasing from front to back.
    Each i is a viable start for some future subarray ending at t ≥ j.

    No index in starts is dominated by another.
    Every subarray starting at an index < starts[0] and ending at any index < j has already been considered and cannot yield a shorter valid answer.
"""
