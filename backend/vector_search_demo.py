# backend/vector_search_demo.py
import math
from typing import List, Dict
from vector_store import EducationalVectorStore

"""
=====================================================================
Module 9: Educational Vector Search Demonstration
=====================================================================

Why this file exists:
    To showcase a complete end-to-end Vector Search pipeline for learning:
    1. User Question is entered.
    2. Query is converted into a vector (Mock Embedding).
    3. The Vector Store searches for nearest neighbors.
    4. Displays the Top 3 matches and selects the best one.
"""

# =====================================================================
# Mock Database Entries with 2D Vector Embeddings
# Dimension 1 (X): Finance / Loan affinity
# Dimension 2 (Y): Sports / Leisure affinity
# =====================================================================
EDUCATIONAL_DATABASE = [
    {
        "id": 1,
        "question": "What is EMI?",
        "vector": [0.95, 0.05],
        "answer": "Equated Monthly Installment (EMI) is a fixed payment amount made by a borrower to a lender at a specified date each calendar month."
    },
    {
        "id": 2,
        "question": "What is a Home Loan?",
        "vector": [0.92, 0.08],
        "answer": "A Home Loan is a secured loan product designed to help individuals purchase, construct, or renovate a residential property."
    },
    {
        "id": 3,
        "question": "What is a Vehicle Loan?",
        "vector": [0.90, 0.10],
        "answer": "A Vehicle Loan helps you finance the purchase of a new or pre-owned car, motorcycle, or commercial vehicle."
    },
    {
        "id": 4,
        "question": "Where is the head office?",
        "vector": [0.50, 0.50],
        "answer": "Our corporate head office is located in Connaught Place, New Delhi."
    },
    {
        "id": 5,
        "question": "Do you play football?",
        "vector": [0.15, 0.85],
        "answer": "We are a banking assistant, but we love football! Many of our employees participate in annual corporate league matches."
    },
    {
        "id": 6,
        "question": "Is cricket popular in India?",
        "vector": [0.05, 0.95],
        "answer": "Yes, cricket is exceptionally popular in India and has a massive fan base."
    }
]


# =====================================================================
# Mock Embedding Generator
# =====================================================================
def get_mock_embedding(text: str) -> List[float]:
    """
    Purpose:
        Map a natural language query to a 2D vector coordinate based on keyword weights,
        simulating a semantic embedding model.
    Input:
        text (str): The raw string question from the user.
    Output:
        List[float]: A 2D normalized vector representing the query coordinates.
    Flow:
        1. Tokenizes text to lowercase words.
        2. Accumulates raw score weights:
           - Adds weight to Finance axis if terms like "emi", "loan", "interest", "bank" exist.
           - Adds weight to Sports axis if terms like "football", "cricket", "play", "match" exist.
        3. Sets a small base weight to prevent zero-magnitude vectors.
        4. Normalizes coordinates to unit length (vector magnitude = 1.0) so Cosine Similarity calculations work properly.
    """
    words = text.lower().strip().split()
    
    finance_weight = 0.05
    sports_weight = 0.05
    
    finance_terms = {"emi", "loan", "loans", "interest", "rates", "cibil", "borrow", "lender", "bank"}
    sports_terms = {"football", "cricket", "play", "sports", "games", "match", "league"}
    
    for word in words:
        # Strip trailing punctuation
        clean_word = "".join(c for c in word if c.isalnum())
        if clean_word in finance_terms:
            finance_weight += 0.90
        if clean_word in sports_terms:
            sports_weight += 0.90
            
    # Calculate Magnitude (Euclidean norm)
    mag = math.sqrt(finance_weight**2 + sports_weight**2)
    
    # Return normalized unit vector
    return [finance_weight / mag, sports_weight / mag]


# =====================================================================
# Main Demonstration Runner
# =====================================================================
def main():
    print("=" * 80)
    print("                VECTOR DATABASE SEARCH PIPELINE DEMONSTRATION")
    print("=" * 80)
    
    # 1. Initialize Educational Vector Store
    v_db = EducationalVectorStore()
    v_db.load_vectors(EDUCATIONAL_DATABASE)
    print("-" * 80)
    
    # 2. Run Test Queries
    test_queries = [
        "How do I pay my monthly emi loan?",
        "Do you sponsor any cricket tournaments?",
        "corporate head office information"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Scenario {i}: User asks: '{query}' ---")
        
        # Step A: Generate Embedding Vector
        query_vector = get_mock_embedding(query)
        print(f"  [1. Embedding Generator] Converted text to 2D vector: {query_vector}")
        
        # Step B: Perform Nearest Neighbor Top-K Search
        top_matches = v_db.top_k_search(query_vector, k=3)
        
        # Step C: Print Search Results
        print("  [2. Vector Similarity Search] Top 3 closest entries:")
        for idx, (record, score) in enumerate(top_matches, 1):
            print(f"     Match {idx}: Question: {record['question']:30} | Vector: {record['vector']} | Similarity Score: {score*100:6.2f}%")
            
        # Step D: Select Final Answer
        best_record, best_score = top_matches[0]
        print(f"\n  [3. Selection] Highest matching score is {best_score*100:.2f}% (Record ID: {best_record['id']})")
        print(f"  [4. Final Bot Response]:\n     \"{best_record['answer']}\"")
        print("-" * 80)

if __name__ == "__main__":
    main()
