# Problem — Sliding Window (Invariant-first)

# Smallest Subarray With Sum ≥ K

# You are given:
# An array A of positive integers
# A positive integer K

# Your task is to find the minimum length of a contiguous subarray whose sum is at least K.
# If no such subarray exists, return 0.

# Example:

# A = [2, 3, 1, 2, 4, 3]
# K = 7
# Output = 2   # [4, 3]

# Constraints (read carefully)
# All numbers are positive (this matters a lot)
# We are aiming for O(n) time
# No brute force
# No nested scanning
# No flags
# The invariant must explain:
#   expansion
#   contraction

# why correctness is preserved
# Your task (exactly this order)
# 1️⃣ State / pointers

# What pointers do you maintain, and what does each mean?
# 2️⃣ Invariant

# A precise statement that is true at the start of every iteration.
# This is the hard part.
# 3️⃣ Completion & failure encoding
# How do you know the answer is final?
# How is “no valid subarray” represented without extra checks?

# One hint (only one)

# Because all numbers are positive, the window sum behaves monotonically in one direction.
# Your invariant should exploit that fact.

# left
# → leftmost index of the sliding window
# right points to the next element to be added to the window
# (i.e., the window is A[left : right], right-exclusive)
# Why this matters:
#     It avoids off-by-one confusion
#     It makes expansion = add A[right]; right += 1
#     It aligns perfectly with invariant reasoning
# So your window is always:
#     A[left : right]
# sum
# → sum of elements in the current window
# cached best solution
# → length of the smallest valid window seen so far

# Invariant:
# At the start of each iteration, the window A[left : right] has sum sum, and
# all subarrays that end before right have already been considered
# if sum ≥ K, then shrinking from the left is the only way to possibly find a shorter valid subarray ending at right
# Or in slightly plainer English:
# Everything smaller than this window has already been checked, and once the sum is big enough, the only remaining optimization is to shrink.

# That’s the invariant doing the thinking.
# Why expanding is always safe
# Because:
# All numbers are positive
# If sum < K, no subarray starting at left and ending before right can work
# So shrinking would only make things worse

# Therefore:
# Expand until sum ≥ K
# Do not even consider shrinking before that
# This is not a rule — it’s a consequence of the invariant.
# Why shrinking is safe (and necessary)
# Once sum ≥ K, any subarray that starts left of left and ends at right is longer than the current one — so it cannot be optimal.

# Therefore:
# Shrinking may improve the answer
# Not shrinking would miss shorter valid windows
# This is the critical sliding-window insight.

# Completion & failure

# Completion:
# When right reaches the end, no new windows can be formed.

# Failure:
# If you never observed sum ≥ K, your cached answer stays at its sentinel value → return 0.
# Failure is encoded in state, not checks.


def minSubArrayLen(K, A):
    left = 0
    current_sum = 0
    best = float("inf")
    for right in range(len(A)):
        current_sum += A[right]
        while current_sum >= K:
            best = min(best, right - left + 1)
            current_sum -= A[left]
            left += 1
    return 0 if best == float("inf") else best


def minSubArray(K, A):
    left = 0
    current_sum = 0
    best_len = float("inf")
    best = []
    for right in range(len(A)):
        current_sum += A[right]
        while current_sum >= K:
            if not best or (right - left + 1) < best_len:
                best_len = right - left + 1
                best = [left, right]
            current_sum -= A[left]
            left += 1
    return A[best[0] : best[1] + 1]


print(minSubArrayLen(15, [4, 5, 2, 7, 2, 6, 8, 1, 7, 9, 6]))
print(minSubArray(15, [4, 5, 2, 7, 2, 6, 8, 1, 7, 9, 6]))
