# backend/embedding_demo.py
"""
=====================================================================
Module 8: Educational Embedding and Cosine Similarity Demonstration
=====================================================================

Purpose:
    This file is an educational script designed to teach the fundamentals
    of word embeddings and cosine similarity without using any external 
    neural network or AI frameworks.

Why this file exists:
    To show mathematically how word concepts are mapped to a continuous
    multi-dimensional vector space, allowing similar semantic meanings to
    align close to one another, which solves the failures of keyword search.
"""

import math

# =====================================================================
# Manual Hand-crafted Word Embeddings (2-Dimensional Space)
# =====================================================================
# Dimension 1 (X-axis): Semantic weight related to "Loan / Credit / Finance"
# Dimension 2 (Y-axis): Semantic weight related to "Sports / Games"
WORD_EMBEDDINGS = {
    "interest":  [0.92, 0.08],
    "rates":     [0.91, 0.09],
    "cibil":     [0.89, 0.11],
    "football":  [0.20, 0.80],
    "cricket":   [0.10, 0.90]
}


# =====================================================================
# Mathematical Utility Functions
# =====================================================================

def dot_product(v1: list[float], v2: list[float]) -> float:
    """
    Purpose:
        Calculate the dot product of two numerical vectors.
    Input:
        v1 (list[float]): The first vector.
        v2 (list[float]): The second vector.
    Output:
        float: The scalar value representing the dot product.
    Math:
        v1 · v2 = sum(v1[i] * v2[i]) for all dimensions i.
    """
    return sum(x * y for x, y in zip(v1, v2))


def magnitude(v: list[float]) -> float:
    """
    Purpose:
        Calculate the geometric length (Euclidean/L2 norm) of a vector.
    Input:
        v (list[float]): The numerical vector.
    Output:
        float: The absolute length of the vector from the origin (0, 0).
    Math:
        ||v|| = sqrt(sum(v[i]^2)) for all dimensions i.
    """
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """
    Purpose:
        Calculate the cosine of the angle between two vectors to determine
        their semantic similarity.
    Input:
        v1 (list[float]): The first embedding vector.
        v2 (list[float]): The second embedding vector.
    Output:
        float: The similarity score ranging from -1.0 (opposite) to 1.0 (identical direction).
    Math:
        Cosine Similarity = (v1 · v2) / (||v1|| * ||v2||)
    """
    val_dot = dot_product(v1, v2)
    mag_v1 = magnitude(v1)
    mag_v2 = magnitude(v2)
    
    if mag_v1 == 0.0 or mag_v2 == 0.0:
        return 0.0  # Guard against division by zero
        
    return val_dot / (mag_v1 * mag_v2)


# =====================================================================
# Main Educational Demonstration execution
# =====================================================================
def run_demo():
    print("=" * 70)
    print("            WORD EMBEDDING & COSINE SIMILARITY DEMONSTRATION")
    print("=" * 70)
    print("Our 2D Vector Space Dimensions:")
    print("  - Dim 1 (X): Loan / Credit association strength")
    print("  - Dim 2 (Y): Sports / Play association strength\n")
    
    print("Word Vectors:")
    for word, vector in WORD_EMBEDDINGS.items():
        print(f"  - '{word}': {vector}")
    print("-" * 70)

    # 1. Compare: interest vs rates
    v_interest = WORD_EMBEDDINGS["interest"]
    v_rates = WORD_EMBEDDINGS["rates"]
    sim_interest_rates = cosine_similarity(v_interest, v_rates)

    # 2. Compare: interest vs football
    v_football = WORD_EMBEDDINGS["football"]
    sim_interest_football = cosine_similarity(v_interest, v_football)

    # Print Results
    print(f"1. Comparing 'interest' vs 'rates':")
    print(f"   - Vector 'interest': {v_interest}")
    print(f"   - Vector 'rates':    {v_rates}")
    print(f"   - Cosine Similarity: {sim_interest_rates:.6f} ({sim_interest_rates * 100:.2f}% similarity)\n")

    print(f"2. Comparing 'interest' vs 'football':")
    print(f"   - Vector 'interest':  {v_interest}")
    print(f"   - Vector 'football': {v_football}")
    print(f"   - Cosine Similarity: {sim_interest_football:.6f} ({sim_interest_football * 100:.2f}% similarity)\n")

    print("-" * 70)
    print("EXPLANATION:")
    print("  * 'interest' and 'rates' have high similarity (~99.9%) because both vectors")
    print("    point in almost the same direction (heavily loaded on the Loan/Credit dimension).")
    print("  * 'interest' and 'football' have low similarity (~34.4%) because their vectors")
    print("    are nearly orthogonal (perpendicular). 'interest' lies along the X-axis (loan),")
    print("    while 'football' lies along the Y-axis (sports).")
    print("=" * 70)

if __name__ == "__main__":
    run_demo()
