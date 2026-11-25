# #AlgoExpert
# Valid Subsequence -
# Given two non-empty arrays of integers, write a function that determines whether the second array is a subsequence of the first one. A subsequence of an array is a set of numbers that aren't necessarily adjacent in the array but that are in the same order as they appear in the array.

# For instance, the numbers [1, 3, 4] form a subsequence of the array [1, 2, 3, 4], and so do the numbers [2, 4].

# Note that a single number in an array and the array itself are both valid subsequences of the array.

# Sample Input:
# array = [5, 1, 22, 25, 6, -1, 8, 10]
# sequence = [1, 6, -1, 10]

# Sample Output:
# true


# First attempt
def isValidSubsequence1(array, sequence):
    left = 0

    for num in sequence:
        match = False
        while not match and left < len(array):
            if num == array[left]:
                match = True
            left += 1
        # Following necessary check was first missed leading to bugs
        if not match:
            return False

    return True


# Complexity analysis (let’s be precise)
# Time complexity

# n = len(array)
# m = len(sequence)

# The algorithm:
# left only moves forward
# never resets
# visits each element of array at most once

# ✅ Time: O(n)
# (Strictly speaking O(n + m), but O(n) is acceptable and standard.)

# Space complexity
# ✅ O(1)
# No extra data structures, just pointers and flags.

# Feedback-
# Mentor note (this is important)
# You’re thinking in control flow, not brute force.
# You just didn’t explicitly encode the failure condition.

# That’s not a logic flaw — it’s a boundary enforcement issue.
# The next level up is learning to ask yourself:

# “What must be true after this loop ends?”
# That habit alone levels you up fast.

# Next steps now:

#     1. Refactor this into the canonical minimal solution (even cleaner)
#     2. Talk about loop invariants explicitly (very interview-useful)
#     3. Show how this pattern appears in streaming data / ML preprocessing
#     4. Stress-test with edge cases

# 1️⃣ Canonical minimal solution (cleanest form)
# Idea
#     One pointer for sequence
#     Scan through array
#     Advance sequence pointer only when you match


def isValidSubsequence2(array, sequence):
    seq_idx = 0
    for num in array:
        if seq_idx == len(sequence):
            break
        if num == sequence[seq_idx]:
            seq_idx += 1
    return seq_idx == len(sequence)


# Why this is better
#     Fewer variables
#     No nested while
#     Failure is naturally encoded
#     Reads like English

# 2️⃣ Loop invariants (this is the real lesson)
# A loop invariant is something that is always true at a specific point in the loop.
# Invariant here
# At the start of each iteration of the for loop:

# sequence[:seq_idx] has already been found in order in array up to the current position.

# That’s why:
#     We never decrement seq_idx
#     We never revisit elements
#     At the end, checking seq_idx == len(sequence) is sufficient

# Your original bug happened because:
#     The invariant “current sequence element must be matched” was not enforced

# Once you start thinking in invariants, bugs like that disappear.

# 3️⃣ How this shows up in ML / data pipelines
# This pattern is everywhere in ML, just dressed differently.

# Examples
#     Aligning labels with time-series data
#     Verifying event order in logs
#     Checking monotonic sequences in preprocessing
#     Matching tokens in NLP streams
#     Validating curriculum ordering in training data

# All of these reduce to:
#     “Can I consume stream A while matching ordered constraints from stream B?”

# Same two-pointer logic.
#     If you master this pattern, preprocessing stops being scary.

# 4️⃣ Edge cases & stress tests (interview gold)
# Let’s test your mental model:
# Edge case 1
# array = [1, 2, 3]
# sequence = []
# ✔ Always True (empty sequence is valid)

# Edge case 2
# array = []
# sequence = [1]
# ✔ False

# Edge case 3
# array = [1, 1, 1, 1]
# sequence = [1, 1]
# ✔ True
# Your canonical solution handles all of these without special code.

# Big-picture takeaway (this matters):
# This wasn’t about subsequences.
# You just learned:
#     how to enforce loop invariants
#     how to encode failure implicitly
#     how to reason about one-pass algorithms
#     how interviewers think

# That’s a real step forward.

# Next time, I’ll start pushing you to state invariants before coding.
# That’s the habit that separates “knows Python” from “thinks like an engineer.”

# When you’re ready, say the word and we’ll move to the next problem or tie this into NumPy/vectorization.

print(isValidSubsequence2([1, 1, 1, 1], [1, 1]))
