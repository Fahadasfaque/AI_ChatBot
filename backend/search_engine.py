import os
import random
import json
import re
from rapidfuzz import fuzz

# =====================================================================
# Reference Vocabulary for Spelling Correction
# =====================================================================
VOCABULARY = {
    # Greetings & Appreciation
    "hi", "hello", "hey", "yo", "hola", "hlw", "hiya", "sup", "bonjour", "namaste", "greetings", "good", 
    "morning", "afternoon", "evening", "night", "day", "gm", "gn", "thanks", "thank", "thx", "appreciate",
    "welcome", "pleasure", "assist", "assistance",
    # Intents & Knowledge Base keywords (Loan Origination System)
    "loans", "loan", "products", "home", "personal", "vehicle", "car", "education", "business", "gold",
    "eligibility", "eligible", "criteria", "qualify", "qualification", "cibil", "credit", "score", "rating",
    "document", "documents", "doc", "docs", "paperwork", "proof", "income", "salary", "slips", "pan", "aadhaar", "itr", "deed",
    "interest", "rate", "rates", "roi", "percentage", "charges", "emi", "installment", "installments", "repayment", "monthly", "payment", "calculator",
    "workflow", "process", "procedure", "apply", "origination", "sanction", "disbursement", "status", "track", "progress", "application", "id", "register", "form", "fill",
    "occupation", "employer", "tenure", "property", "value", "salaried", "self-employed", "support", "contact", "email", "phone", "branch", "manager", "helpline", "toll", "free", "nodal", "officer", "customer", "care",
    # Context queries
    "what", "is", "where", "who", "when", "live", "choose", "select", "tell", "show", "last", "past",
    # Common helper words / pronouns / grammar particles (to prevent false corrections)
    "my", "i", "me", "you", "your", "we", "our", "he", "she", "it", "they", "them",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "a", "an", "the", "and", "but", "or", "if", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", 
    "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
    "than", "too", "very", "s", "t", "can", "will", "just", "should", "now"
}

# =====================================================================
# spelling corrector function
# =====================================================================
def correct_spelling(message: str) -> str:
    """
    Purpose:
        Perform spelling correction on misspelled words in the user message
        by matching them against our known vocabulary using RapidFuzz.

    Input:
        message (str): The raw user message.

    Output:
        str: The corrected user message.

    How score is calculated:
        Uses rapidfuzz.fuzz.ratio to measure character similarity between
        the user's word and the vocabulary words. If the highest score is
        >= 80.0%, we replace the word with the vocabulary match.
    """
    if not message:
        return message
        
    words = message.split()
    corrected_words = []
    
    for word in words:
        # Strip trailing punctuation from the word for checking
        cleaned_word = re.sub(r"[?!.,:;()\[\]{}]", "", word)
        
        # Skip if word is empty, has digits, contains '@' (email), or is already in vocabulary
        if not cleaned_word or any(c.isdigit() for c in cleaned_word) or "@" in cleaned_word:
            corrected_words.append(word)
            continue
            
        word_lower = cleaned_word.lower()
        if word_lower in VOCABULARY:
            corrected_words.append(word)
            continue
            
        # Find the best match in the vocabulary
        best_match = None
        best_ratio = -1.0
        
        for vocab_word in VOCABULARY:
            ratio = fuzz.ratio(word_lower, vocab_word)
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = vocab_word
                
        # If match is strong (>= 80%), correct the word while preserving original case/punctuation structure
        if best_match and best_ratio >= 80.0:
            # Preserve case (Title case if original was title case, upper if upper, etc.)
            if cleaned_word.isupper():
                corrected_word = best_match.upper()
            elif cleaned_word[0].isupper():
                corrected_word = best_match.capitalize()
            else:
                corrected_word = best_match
                
            # Put punctuation back
            prefix = word[:word.find(cleaned_word)]
            suffix = word[word.find(cleaned_word) + len(cleaned_word):]
            corrected_words.append(prefix + corrected_word + suffix)
        else:
            corrected_words.append(word)
            
    return " ".join(corrected_words)


# =====================================================================
# helper: clean_and_tokenize
# =====================================================================
def clean_and_tokenize(text: str) -> set[str]:
    """
    Purpose:
        Preprocess text by lowercasing, stripping common punctuation marks,
        and splitting into a set of unique word tokens.

    Input:
        text (str): The raw input sentence or key phrase.

    Output:
        set[str]: A set of lowercase, clean words.

    How score is calculated:
        N/A (This is a text preprocessing helper).
    """
    if not text:
        return set()
    
    # Lowercase the entire text
    text_lower = text.lower().strip()
    
    # Strip common punctuation characters using regex
    clean_text = re.sub(r"[?!.,:;()\[\]{}'\"\-_\/]", " ", text_lower)
    
    # Split into words and return as a set
    words = clean_text.split()
    return set(words)


# =====================================================================
# calculate_similarity_score
# =====================================================================
def calculate_similarity_score(query_tokens: set[str], candidate_tokens: set[str]) -> float:
    """
    Purpose:
        Calculate a percentage score showing how well a candidate question/topic
        matches the user's query using fuzzy word Jaccard similarity.

    Input:
        query_tokens (set[str]): Preprocessed word tokens from the user's query.
        candidate_tokens (set[str]): Preprocessed word tokens from the candidate topic.

    Output:
        float: Similarity percentage score from 0.0 to 100.0.

    How score is calculated:
        We measure the fuzzy intersection (matching_count) and divide by the union
        of the query and candidate tokens.
        Score = (Matching Words / (Query Words + Candidate Words - Matching Words)) * 100
        
        If candidate_tokens or query_tokens is empty, returns 0.0.
    """
    if not candidate_tokens or not query_tokens:
        return 0.0
        
    matching_count = 0
    # For each word in the candidate, check if there's a fuzzy matching word in the query
    for c_word in candidate_tokens:
        for q_word in query_tokens:
            if fuzz.ratio(q_word, c_word) >= 80.0:
                matching_count += 1
                break
                
    union_count = len(query_tokens) + len(candidate_tokens) - matching_count
    if union_count <= 0:
        return 0.0
        
    score = (matching_count / union_count) * 100.0
    return score


# =====================================================================
# build_search_candidates
# =====================================================================
def build_search_candidates(kb: dict) -> list[dict]:
    """
    Purpose:
        Flatten the structured knowledge base files into a list of searchable
        question-answer candidates.

    Input:
        kb (dict): Loaded knowledge base content mapping filenames to data.

    Output:
        list[dict]: A list of candidate dictionaries. Each candidate has:
            - "question": The search query to match against.
            - "answer": The answer string to return if matched.
            - "source": The category name/file source.
    """
    candidates = []

    # Iterate through the 9 knowledge categories and load questions
    for key in [
        "loan_products", "loan_faq", "loan_workflow", "loan_documents",
        "eligibility", "interest_rates", "emi_information", "customer_support",
        "company"
    ]:
        data = kb.get(key, {})
        for question, answer in data.items():
            candidates.append({
                "question": question,
                "answer": answer,
                "source": key
            })

    return candidates


# =====================================================================
# search_kb
# =====================================================================
def search_kb(query: str, kb: dict) -> tuple[str, float, str] | None:
    """
    Purpose:
        Search all knowledge base candidates for a user query, calculate
        similarity scores, and return the highest-scoring candidate.

    Input:
        query (str): The user's input query.
        kb (dict): Loaded knowledge base dictionary.

    Output:
        tuple[str, float, str] | None: A tuple containing:
            1. The best matching answer text.
            2. The matching percentage score (0.0 to 100.0).
            3. The source intent category (e.g. "pricing", "faq").
            Returns None if no candidates could be matched or evaluated.

    How score is calculated:
        1. Tokenizes the user query into query_tokens.
        2. Tokenizes each candidate question into candidate_tokens.
        3. Invokes calculate_similarity_score() for each candidate.
        4. Tracks the candidate with the highest similarity score.
        5. Breaks ties by returning the first occurrence in the candidate list.
    """
    print(f"      ▶ [search_engine.py:search_kb] Called with query={query!r}")
    query_tokens = clean_and_tokenize(query)
    if not query_tokens:
        print("        [Search Engine] Query is empty after tokenization.")
        print("      ◀ [search_engine.py:search_kb] Returning None")
        return None

    candidates = build_search_candidates(kb)
    best_candidate = None
    best_score = -1.0

    print(f"        - Tokenized Query: {query_tokens}")
    print(f"        - Searching {len(candidates)} candidates...")

    # Iterate and rank every candidate
    clean_query = "".join(c for c in query.lower() if c.isalnum() or c.isspace()).strip()

    for cand in candidates:
        clean_question = "".join(c for c in cand["question"].lower() if c.isalnum() or c.isspace()).strip()
        if clean_query == clean_question:
            score = 100.0
        else:
            cand_tokens = clean_and_tokenize(cand["question"])
            score = calculate_similarity_score(query_tokens, cand_tokens)
        
        # Print score debug logs for tracking
        if score > 0.0:
            cand_tokens = clean_and_tokenize(cand["question"])
            matched_subset = [c_word for c_word in cand_tokens if any(fuzz.ratio(q_word, c_word) >= 80.0 for q_word in query_tokens)]
            print(f"          - Score: {score:5.1f}% | Overlap: {set(matched_subset)} | Cand: {cand['question'][:40]:40}")
            
        # Keep track of highest score
        if score > best_score:
            best_score = score
            best_candidate = cand

    if best_candidate and best_score > 0.0:
        print(f"        - Best Match Score: {best_score:.1f}%")
        print(f"      ◀ [search_engine.py:search_kb] Returning: (answer={best_candidate['answer']!r}, score={best_score:.1f}%, source={best_candidate['source']!r})")
        return best_candidate["answer"], best_score, best_candidate["source"]
  
    print("        - No matches found with score > 0%")
    print("      ◀ [search_engine.py:search_kb] Returning None")
    return None
