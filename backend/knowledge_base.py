# backend/knowledge_base.py - updated for LOS conversion
"""
Purpose:
    This file implements the rule-based Knowledge Base for our chatbot.
    It loads structured static knowledge from JSON files and performs
    simple keyword-matching searches to retrieve answers.

Why this file exists:
    Instead of hardcoding details like pricing, FAQs, and company info directly
    in the code, storing them in external JSON files separates data from logic.
    The Knowledge Base serves as the module to load, search, and retrieve this data.

How it works:
    1. Reads JSON files from the 'knowledge/' directory on start (or on query).
    2. Given a query, intent, and extracted entities:
       - If intent is "pricing", looks up matching product prices in pricing.json.
       - If intent is "support" or "contact", looks up details in support.json.
       - Otherwise, performs substring keyword matching across all keys in
         pricing.json, faq.json, support.json, products.json, and company.json.
    3. Returns the matching value as a string, or None if no match is found.

Input:
    query (str): The raw text message submitted by the user.
    intent_name (str): The name of the detected intent.
    entities (dict): A dictionary of extracted entities (e.g. name, amount, product).

Output:
    str | None: The matching knowledge text if found, otherwise None.
"""

import os
import json
import search_engine

# Get the directory of the current script to locate the knowledge folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

# Loaded knowledge cache
_knowledge_cache = {}


def load_knowledge_files() -> dict:
    """
    Why it exists:
        Loads all JSON files in the knowledge/ folder into memory.
    
    Input:
        None

    Output:
        dict: A dictionary mapping file names (without .json extension) to their parsed JSON content.
              Example: {"pricing": {...}, "faq": {...}}
              
    Flow:
        1. Checks if the global cache is empty.
        2. If empty, iterates through all files in KNOWLEDGE_DIR.
        3. Parses every .json file and saves it in the cache dictionary.
        4. Returns the cache.
    """
    global _knowledge_cache
    if not _knowledge_cache:
        print("      ▶ [knowledge_base.py:load_knowledge_files] Loading JSON files from disk...")
        if not os.path.exists(KNOWLEDGE_DIR):
            print(f"        [WARNING] Knowledge directory not found at: {KNOWLEDGE_DIR}")
            return {}
            
        for filename in os.listdir(KNOWLEDGE_DIR):
            if filename.endswith(".json"):
                key = filename[:-5]  # Strip '.json'
                filepath = os.path.join(KNOWLEDGE_DIR, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        _knowledge_cache[key] = json.load(f)
                    print(f"        - Loaded: {filename} ({len(_knowledge_cache[key])} keys)")
                except Exception as e:
                    print(f"        - [ERROR] Failed to load {filename}: {e}")
                    
    return _knowledge_cache


def query_knowledge_base(query: str, intent_name: str, entities: dict) -> tuple[str | None, float | None]:
    """
    Why it exists:    
        Searches the loaded knowledge files by calling our Search and Ranking Engine.
        
    Input:
        query (str): The user's original raw message.
        intent_name (str): The detected intent name.
        entities (dict): Dictionary of extracted entities.
        
    Output:
        tuple[str | None, float | None]: A tuple of:
            - The matching info string (or None if no match).
            - The similarity score of the match (or None if no match).
        
    Flow:
        1. Ensure knowledge files are loaded into memory.
        2. Delegate search and ranking to search_engine.search_kb().
        3. If similarity score is >= 30.0%, return the matched answer and score.
        4. Otherwise, return (None, None).
    """
    print(f"      ▶ [knowledge_base.py:query_knowledge_base] Called with query={query!r}, intent_name={intent_name!r}, entities={entities!r}")
    
    # 1. Load knowledge cache
    kb = load_knowledge_files()
    print("[KB] : ",kb) 
    if not kb:
        print("      ◀ [knowledge_base.py:query_knowledge_base] Returning None (KB empty or not found)")
        return None, None

    # 2. Call Search Engine to rank candidates and find the best match
    search_result = search_engine.search_kb(query, kb)
    if search_result:
        answer, score, source = search_result
        # If the similarity score is high enough (>= 30.0%), return the answer and score
        if score >= 30.0:
            print(f"        - Search Engine found relevant match in {source!r} with score {score:.1f}%")
            print(f"      ◀ [knowledge_base.py:query_knowledge_base] Returning: (answer={answer!r}, score={score:.1f}%)")
            return answer, score
        else:
            print(f"        - Match in {source!r} has score {score:.1f}%, which is below threshold of 30.0%")

    print("        - No relevant search engine match found.")
    print("      ◀ [knowledge_base.py:query_knowledge_base] Returning (None, None)")
    return None, None
