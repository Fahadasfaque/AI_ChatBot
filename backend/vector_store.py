# backend/vector_store.py
import math
from typing import List, Dict, Tuple, Optional

"""
=====================================================================
Module 9: Educational In-Memory Vector Store
=====================================================================

Why this file exists:
    To teach the core mechanics of a Vector Database from scratch.
    This file demonstrates how vectors are stored in memory, how
    similarity metrics like Cosine Similarity are computed, and how
    algorithms search for the Nearest Neighbors (Top-K) to locate
    semantically matching queries.

How it works:
    1. Holds a list of vector records in-memory.
    2. Computes the cosine angle between a query vector and database vectors.
    3. Sorts records by highest similarity score to return the top results.
"""

class EducationalVectorStore:
    def __init__(self):
        """
        Purpose:
            Initialize an empty in-memory vector store database.
        Input:
            None
        Output:
            None
        Flow:
            Creates an empty list 'self.records' to hold record dicts containing
            ids, questions, raw vectors, and answers.
        """
        self.records: List[Dict] = []

    def store_vector(self, record_id: int, question: str, vector: List[float], answer: str) -> None:
        """
        Purpose:
            Insert a new text item along with its pre-computed embedding vector 
            and corresponding answer into the database.
        Input:
            record_id (int): A unique identifier for the entry.
            question (str): The text question (e.g. "What is EMI?").
            vector (List[float]): The high-dimensional embedding array representing the question.
            answer (str): The corresponding answer to return if matched.
        Output:
            None
        Flow:
            1. Wraps parameters into a structured dictionary.
            2. Appends the dictionary to self.records.
        """
        record = {
            "id": record_id,
            "question": question,
            "vector": vector,
            "answer": answer
        }
        self.records.append(record)
        print(f"[Vector Store] Stored record {record_id}: {question!r} (Dim: {len(vector)})")

    def load_vectors(self, dataset: List[Dict]) -> None:
        """
        Purpose:
            Bulk-load a list of pre-configured records into the database.
        Input:
            dataset (List[Dict]): A list of dictionaries, where each dict contains
                                  "id", "question", "vector", and "answer".
        Output:
            None
        Flow:
            1. Loops over each record in the dataset list.
            2. Invokes store_vector() on each record to populate the database.
        """
        print(f"[Vector Store] Loading {len(dataset)} records in bulk...")
        for item in dataset:
            self.store_vector(
                record_id=item["id"],
                question=item["question"],
                vector=item["vector"],
                answer=item["answer"]
            )

    def calculate_cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """
        Purpose:
            Measure the cosine of the angle between two numerical vectors to calculate
            their semantic similarity.
        Input:
            v1 (List[float]): The first vector coordinates.
            v2 (List[float]): The second vector coordinates.
        Output:
            float: Similarity score ranging from -1.0 (opposite directions) to 1.0 (identical direction).
        Flow:
            1. Checks that the two vectors have matching dimensions.
            2. Calculates the Dot Product: sum(x * y) for all dimensions.
            3. Calculates the Magnitude (length) of v1: sqrt(sum(x^2)).
            4. Calculates the Magnitude (length) of v2: sqrt(sum(y^2)).
            5. Returns (dot_product) / (mag_v1 * mag_v2), guarding against division by zero.
        """
        if len(v1) != len(v2):
            raise ValueError(f"Vector dimensions must match. Got {len(v1)} and {len(v2)}.")

        # 1. Calculate Dot Product
        dot_product = sum(x * y for x, y in zip(v1, v2))

        # 2. Calculate Magnitudes
        magnitude_v1 = math.sqrt(sum(x * x for x in v1))
        magnitude_v2 = math.sqrt(sum(y * y for y in v2))

        # 3. Compute Cosine Similarity
        if magnitude_v1 == 0.0 or magnitude_v2 == 0.0:
            return 0.0

        return dot_product / (magnitude_v1 * magnitude_v2)

    def nearest_neighbor_search(self, query_vector: List[float]) -> Optional[Dict]:
        """
        Purpose:
            Find the single closest matching entry in the database for a query vector.
        Input:
            query_vector (List[float]): The vector of the user's query.
        Output:
            Dict | None: The record dictionary that is closest to the query vector,
                         or None if the database is empty.
        Flow:
            1. Reuses top_k_search(query_vector, k=1) to retrieve the top match.
            2. Returns the record dictionary if a match exists, otherwise None.
        """
        results = self.top_k_search(query_vector, k=1)
        if results:
            record, similarity_score = results[0]
            return record
        return None

    def top_k_search(self, query_vector: List[float], k: int = 3) -> List[Tuple[Dict, float]]:
        """
        Purpose:
            Perform a search to find the top 'k' most similar records to a query vector.
        Input:
            query_vector (List[float]): The vector of the user's query.
            k (int): The number of closest matches to return (default is 3).
        Output:
            List[Tuple[Dict, float]]: A sorted list of tuples. Each tuple contains:
                                      - The matching record dictionary.
                                      - The cosine similarity score (float).
         Flow:
            1. Loops over all entries stored in self.records.
            2. Computes the cosine similarity between the query_vector and the record's vector.
            3. Pairs the record with its similarity score.
            4. Sorts all pairs in descending order based on the similarity score.
            5. Returns the top 'k' elements from the sorted list.
        """
        scored_records = []
        for record in self.records:
            score = self.calculate_cosine_similarity(query_vector, record["vector"])
            scored_records.append((record, score))

        # Sort based on similarity score in descending order
        scored_records.sort(key=lambda x: x[1], reverse=True)

        return scored_records[:k]
