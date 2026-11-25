# The Problem: Intersection of Three Sorted Arrays
# Given three sorted arrays A, B, and C, return a new array containing only the unique elements that appear in all three.

# Your Task (Invariant-only, no code):

# State the Invariant: What must be true about the output array D relative to the current pointers a_idx, b_idx, and c_idx?

# Pointer Movement Rule: In the two-array version, we moved the pointer that pointed to the smaller value. What is the rule when you have three?

# Completion Logic: When do you stop?

# Take your time to visualize the three pointers moving at different speeds. When you're ready, give me the architecture.

# Next step: State the 3-pointer invariant and movement rules.

# In a truly "canonical" three-pointer intersection, we usually focus on one lead pointer.

# The "Lead" Logic:
#     Check if
#         A[a_idx] == B[b_idx] == C[c_idx]
# If they match: You’ve found a triple intersection. Append to D, then skip duplicates in all three arrays.
# If they don't match: Increment the pointer that is currently pointing to the smallest value.
#     Why? Because that smallest value can never be part of a triple intersection (the other two arrays have already surpassed it).
# Let's sharpen the "Three Pillars"

# The Invariant (Tightened):
#     At the start of each iteration,
#       D contains all unique elements common to A[0:a_idx], B[0:b_idx], and C[0:c_idx].
#     Pointers a_idx, b_idx, c_idx point to the next candidate values.

# The Pointer Movement Rule:
#     If all three values are equal -> Match! (Process & Skip).
#     Otherwise -> Increment the pointer pointing to the minimum of the three values.

# Completion Logic:
#     Stop as soon as any one of the three arrays is exhausted.
#     Reasoning: An intersection requires an element to be in all arrays. If one array is empty, no further intersections are possible.
# Your Next Task (Code Implementation)I want you to write the code for intersect_three(A, B, C).
# Constraints for this implementation:Use the Skip Logic (drain the duplicates at the source).
# Handle the logic using the "Move the Minimum" rule.
# Keep the structure "flat" (avoid deep nesting where possible).
# Before you post:Ask yourself: "What happens if two pointers match but the third is smaller?" (e.g., A=5, B=5, C=2).
# Your logic should naturally handle this without special if cases for "two-way matches."


def intersect_three(A, B, C):
    """
    Finds the intersection of three sorted arrays.

    Args:
        A, B, C: Lists of integers, each sorted in non-decreasing order.

    Returns:
        A list of unique integers present in all three input arrays.

    Invariant:
        D (the result) contains all unique elements common to the prefixes
        processed so far. Pointers always point to the next potential candidate.
    """
    # Initialize pointers
    a_idx, b_idx, c_idx = 0, 0, 0
    d = []

    # Your logic goes here...
    # pass
    # Invariant - At the start of each iteration, D contains all unique elements common to A[0:a_idx], B[0:b_idx], and C[0:c_idx].
    while a_idx < len(A) and b_idx < len(B) and c_idx < len(C):
        if A[a_idx] == B[b_idx] and B[b_idx] == C[c_idx]:
            current_val = A[a_idx]
            d.append(current_val)
            while a_idx < len(A) and A[a_idx] == current_val:
                a_idx += 1
            while b_idx < len(B) and B[b_idx] == current_val:
                b_idx += 1
            while c_idx < len(C) and C[c_idx] == current_val:
                c_idx += 1
        elif A[a_idx] < B[b_idx] and A[a_idx] < C[c_idx]:
            a_idx += 1
        elif B[b_idx] < C[c_idx]:
            b_idx += 1
        else:  # naturally handles the cases like A[a_idx] < B[b_idx] and A[a_idx] == C[c_idx]
            c_idx += 1
    return d


print(intersect_three([1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9], [2, 3, 4, 5], [4, 5, 5, 6, 7]))
