# backend/chatbot.py
"""
Purpose:
    This file defines the Chatbot coordinator. It coordinates the overall
    processing of a user's message by first routing it to the FastPath checks
    (greeting/gibberish) and, if missed, passing it to Intent Detection.

Why this file exists:
    It acts as the single central entry point for the chatbot's message-handling
    pipeline. Callers (like the API router in chat.py) only need to interact with
    this coordinator, keeping them isolated from internal routing details.

How it works:
    1. It first calls process_fastpath() from fastpath.py.
    2. If FastPath detects a "greeting" or "gibberish", it returns that result immediately.
    3. If FastPath returns "echo" (no match), the coordinator passes the message
       to detect_intent() in intent.py to classify the user's query and retrieve
       the correct response.

Input:
    user_message (str): The raw text message submitted by the user.

Output:
    tuple[str, str]: A tuple containing the response text and the category/intent name.
"""

from fastpath import process_fastpath
from intent import detect_intent
from entity import extract_entities
from context import process_context, add_to_history
from response_generator import generate_response
from knowledge_base import query_knowledge_base


# =====================================================================
# get_bot_response Function
# =====================================================================
def get_bot_response(user_message: str, user_id: str = "default_user") -> tuple[str, str, float | None]:
    """
    Why it exists:
        Acts as the central coordinator (the "brain") of the chatbot.
        It runs the sequential chatbot pipeline and prints a beginner-friendly
        step-by-step flowchart to the terminal.
    """
    print(f"    ▶ [chatbot.py:get_bot_response] Called with user_message={user_message!r}, user_id={user_id!r}")

    # Step 0: Apply spelling correction using RapidFuzz
    import search_engine
    corrected_message = search_engine.correct_spelling(user_message)
    if corrected_message != user_message:
        print(f"        - [Spelling] Corrected {user_message!r} -> {corrected_message!r}")
        user_message = corrected_message

    # Step 1: Run FastPath Checks (Rule-based Greetings & Gibberish)
    reply, message_type = process_fastpath(user_message)

    if message_type != "echo":
        # FastPath matched (it is either a greeting or gibberish)
        add_to_history("user", user_message, user_id=user_id)
        add_to_history("bot", reply, user_id=user_id)
        print(f"    ◀ [chatbot.py:get_bot_response] Returning early FastPath response: (reply={reply!r}, message_type={message_type!r}, score=None)")
        return reply, message_type, None

    # Step 2: Run Intent Detection
    intent_name, intent_reply = detect_intent(user_message)

    # Step 3: Run Entity Extraction
    # Entity extraction is decoupled; it adds info without changing the intent.
    entities = extract_entities(user_message)
    name = entities.get("applicant_name") or entities.get("name")

    # Step 4: Run Greeting Fallback Check
    from greeting import starts_with_greeting, get_greeting_response
    is_greeting_start = starts_with_greeting(user_message)
    if intent_name == "UNKNOWN" and is_greeting_start:
        intent_name = "greeting"
        intent_reply = get_greeting_response(user_message, name=name)

    # Step 5: Context Storage (save entities)
    from context import save_context, retrieve_context
    context_reply = save_context(entities, user_id=user_id)

    # Step 6: Context Retrieval (if user asks about previously stored information)
    if context_reply is None:
        context_reply = retrieve_context(user_message, user_id=user_id)
    
    # Step 7: Knowledge Base Search & Ranking (run only if context query did not trigger)
    kb_reply = None
    score = None
    if context_reply is None:
        kb_reply, score = query_knowledge_base(user_message, intent_name, entities)

    # Step 8: Generate Final Response using ResponseGenerator
    response_text, intent_name = generate_response(intent_name, intent_reply, entities, context_reply, kb_reply)

    # Step 9: Log history to session memory
    add_to_history("user", user_message, user_id=user_id)
    add_to_history("bot", response_text, user_id=user_id)

    print(f"    ◀ [chatbot.py:get_bot_response] Returning response: (response_text={response_text!r}, intent_name={intent_name!r}, score={score!r})")
    return response_text, intent_name, score
