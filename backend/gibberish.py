# backend/gibberish.py
"""
Purpose:
    This file contains the logic for detecting gibberish messages.
    Gibberish refers to meaningless inputs like repeating characters ("111111"),
    only special symbols ("@@@@"), or random keyboard mashes ("asdfghjkl").

Why this file exists:
    By filtering out gibberish messages early in the pipeline, we keep our
    intent and entity classification systems accurate and prevent processing
    noise.

How it works:
    We apply a set of simple, linguistically sound rules using Regular Expressions
    and string checks that are easy to explain to a manager:
    1. Empty/Whitespace check.
    2. Pure Symbol Flooding (e.g., "@@@@", ".....").
    3. Single Character Repetition (e.g., "aaaa", "11111").
    4. Syllable/Pattern Repetitions (stuttering patterns like "ababab").
    5. Consonant Clusters (e.g., 6+ consecutive consonants, making the word unpronounceable).
    6. Vowel Clusters (e.g., 5+ consecutive vowels, making the word impossible to pronounce).
    7. Keyboard crawls (sequences of QWERTY keys like "asdf" or "hjkl").

Input:
    message (str): The raw user message.

Output:
    bool: True if gibberish, False otherwise.
"""

import re
import random

# Predefined QWERTY rows to find sequential runs of keys
QWERTY_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]


# =====================================================================
# is_gibberish Function
# =====================================================================
def is_gibberish(message: str) -> bool:
    """
    Why it exists:  
        This is the main function that evaluates a message and returns True
        if it satisfies any of our gibberish detection rules.

    What it receives:
        message (str): The text message sent by the user.

    What it returns:
        bool: True if detected as gibberish, False otherwise.
    """
    print(f"        ▶ [gibberish.py:is_gibberish] Called with message={message!r}")
    # 1. Clean the input and handle empty messages
    cleaned = message.strip()
    if not cleaned:
        print("          - Message is empty/whitespace. Flagged as gibberish.")
        print("        ◀ [gibberish.py:is_gibberish] Returning result=True")
        return True

    # Pre-compiled list of message-level gibberish patterns:
    # Rule 1: Pure Symbol Flooding (e.g. "@@@@", ".....")
    # Rule 2: Single Character Repetition (excluding digits, e.g. "aaaaa", "###")
    # Rule 3: Syllable/Pattern Repetitions (e.g. "ababab", "lalala")
    GIBBERISH_PATTERNS = [
        (r"^[^\w\s]+$", "Rule 1: Pure Symbol Flooding (e.g. '@@@@')"),
        (r"([^\d])\1{2,}", "Rule 2: Single Character Repetition (e.g. 'aaaaa')"),
        (r"(\w{2,3})\1{2,}", "Rule 3: Syllable/Pattern Repetitions (e.g. 'ababab')")
    ]

    cleaned_lower = cleaned.lower()
    for pattern, description in GIBBERISH_PATTERNS:
        if re.search(pattern, cleaned_lower):
            print(f"          - Matched: {description} (Pattern: {pattern!r})")
            print("        ◀ [gibberish.py:is_gibberish] Returning result=True")
            return True

    # 2. Process individual words for linguistic patterns
    words = cleaned_lower.split()
    
    # Word-level patterns:
    # Rule 4: Consonant Clusters (6+ consecutive consonants)
    # Rule 5: Vowel Clusters (5+ consecutive vowels)
    WORD_PATTERNS = [
        (r"[^aeiouy0-9\W_]{6,}", "Rule 4: Consonant Cluster (6+ consonants)"),
        (r"[aeiouy]{5,}", "Rule 5: Vowel Cluster (5+ vowels)")
    ]

    for word in words:
        # Word-level patterns check (Consonant/Vowel clusters) - checked on length >= 5
        if len(word) >= 5:
            for pattern, description in WORD_PATTERNS:
                if re.search(pattern, word):
                    print(f"          - Word {word!r} matched: {description} (Pattern: {pattern!r})")
                    print("        ◀ [gibberish.py:is_gibberish] Returning result=True")
                    return True

        # Rule 6: Keyboard crawls (checked on length >= 4)
        # To avoid false positives on words like "property" (which contains "erty"),
        # we check if the word has 2 or fewer vowels. Most English words with keyboard crawls
        # have 3 or more vowels (e.g. "property", "liberty").
        if len(word) >= 4:
            for i in range(len(word) - 3):
                sub = word[i:i+4]
                for row in QWERTY_ROWS:
                    if sub in row or sub in row[::-1]:
                        vowel_count = sum(1 for c in word if c in "aeiouy")
                        if vowel_count <= 2:
                            print(f"          - Word {word!r} contains keyboard crawl sequence {sub!r} with low vowels ({vowel_count}). Flagged as gibberish.")
                            print("        ◀ [gibberish.py:is_gibberish] Returning result=True")
                            return True

    print("          - Message passed all gibberish rules.")
    print("        ◀ [gibberish.py:is_gibberish] Returning result=False")
    return False


# =====================================================================
# get_gibberish_response Function
# =====================================================================
def get_gibberish_response() -> str:
    """
    Why it exists:
        Returns a polite warning message when gibberish is detected.
        It randomly selects from a set of user-friendly responses.

    What it receives:
        None

    What it returns:
        str: A randomly selected warning text.
    """
    print("        ▶ [gibberish.py:get_gibberish_response] Called (no args)")
    responses = [
        "I couldn't understand your request. Please ask your loan-related question again.",
        "I'm sorry, I didn't understand that. Please ask a question related to loans, eligibility, or documents.",
        "That input is not recognized. Please rephrase your query about our loan products or application status.",
        "I'm unable to process that request. Could you clarify your loan-related inquiry?"
    ]
    result = random.choice(responses)
    print(f"        ◀ [gibberish.py:get_gibberish_response] Returning: {result!r}")
    return result
