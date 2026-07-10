# backend/context.py
"""
Purpose:
    This file implements Conversation Context management for our LOS chatbot.
    It stores and recalls key details (name, loan type, income, amount, employment, etc.)
    over the course of a conversation, and logs the chat history.

Why this file exists:
    Memory enables a natural dialog, allowing the chatbot to answer follow-up queries
    (like "What is my name?" or "What loan did I select?") and verify eligibility
    parameters dynamically.
"""

import re
from typing import Optional

# Simple in-memory session store (dictionary of dictionaries)
sessions = {}

# =====================================================================
# get_session Function
# =====================================================================
def get_session(user_id: str = "default_user") -> dict:
    """
    Why it exists:
        Ensures a user has an active session state initialized in our memory.
    """
    print(f"        ▶ [context.py:get_session] Called with user_id={user_id!r}")
    if user_id not in sessions:
        print(f"          - Session not found. Initializing new session dictionary.")
        sessions[user_id] = {
            "applicant_name": None,
            "loan_type": None,
            "loan_amount": None,
            "monthly_income": None,
            "employment_type": None,
            "occupation": None,
            "employer_name": None,
            "loan_tenure": None,
            "property_value": None,
            "application_id": None,
            "email": None,
            "phone_number": None,
            "pan_number": None,
            "aadhaar_number": None,
            # Backwards compatibility keys
            "name": None,
            "city": None,
            "phone": None,
            "amount": None,
            "product": None,
            "history": []
        }
    
    session = sessions[user_id]
    print(f"        ◀ [context.py:get_session] Returning OLD Session: (Name={session['applicant_name']!r}, Loan={session['loan_type']!r}, Income={session['monthly_income']!r}, Amount={session['loan_amount']!r}, HistoryLength={len(session['history'])})")
    return session


# =====================================================================
# add_to_history Function
# =====================================================================
def add_to_history(role: str, message: str, user_id: str = "default_user") -> None:
    """
    Why it exists:
        Appends a message to the session's chat history.
    """
    print(f"      ▶ [context.py:add_to_history] Called with role={role!r}, message={message!r}, user_id={user_id!r}")
    session = get_session(user_id)
    session["history"].append({
        "role": role,
        "message": message
    })
    print(f"      ◀ [context.py:add_to_history] Logged turn to history. Total turns: {len(session['history'])}")


# =====================================================================
# handle_context_query Function
# =====================================================================
def handle_context_query(message: str, user_id: str = "default_user") -> Optional[str]:
    """
    Why it exists:
        Checks if the user is asking for stored context information and returns it.
    """
    print(f"        ▶ [context.py:handle_context_query] Called with message={message!r}, user_id={user_id!r}")
    message_lower = message.lower().strip()
    session = get_session(user_id)

    # 1. Check for Name queries
    if "what is my name" in message_lower or "what's my name" in message_lower or "do you know my name" in message_lower:
        val = session.get("applicant_name") or session.get("name")
        if val:
            res = f"Your name is {val}."
            print(f"          - Matched Name query. Name stored: {val!r}")
            return res
        fallback = "I don't know your name yet. You can tell me by saying 'My name is [Name]'."
        return fallback

    # 2. Check for Loan Type queries
    if "what loan did i choose" in message_lower or "what loan did i select" in message_lower or "my loan" in message_lower or "what is my loan type" in message_lower:
        val = session.get("loan_type")
        if val:
            res = f"You selected {val} Loan."
            print(f"          - Matched Loan query. Loan stored: {val!r}")
            return res
        fallback = "You haven't selected a loan type yet. You can say 'I want a home loan'."
        return fallback

    # 3. Check for Monthly Income queries
    if "what is my income" in message_lower or "what is my salary" in message_lower or "my income" in message_lower or "my salary" in message_lower or "monthly income" in message_lower:
        val = session.get("monthly_income")
        if val:
            res = f"Your monthly income is ₹{val}."
            print(f"          - Matched Income query. Income stored: {val!r}")
            return res
        fallback = "I don't have your monthly income on file. You can state it by saying 'My monthly income is [Amount]'."
        return fallback

    # 4. Check for Loan Amount queries
    if "what is my loan amount" in message_lower or "how much loan did i request" in message_lower or "my loan amount" in message_lower:
        val = session.get("loan_amount")
        if val:
            res = f"Your requested loan amount is {val}."
            print(f"          - Matched Loan Amount query. Amount stored: {val!r}")
            return res
        fallback = "I don't have your requested loan amount on file. You can state it by saying 'I want a loan of [Amount]'."
        return fallback

    # 5. Check for Employment Type queries
    if "what is my employment type" in message_lower or "my employment" in message_lower:
        val = session.get("employment_type")
        if val:
            res = f"Your employment type is {val}."
            print(f"          - Matched Employment Type query. Type stored: {val!r}")
            return res
        fallback = "I don't have your employment type on file. You can say 'I am salaried' or 'I am self-employed'."
        return fallback

    # 6. Check for Email queries
    if "what is my email" in message_lower or "what's my email" in message_lower or "my email" in message_lower:
        if "my email is" in message_lower or "email is" in message_lower:
            pass  # Let process_context handle updates
        else:
            val = session.get("email")
            if val:
                res = f"Your email is {val}."
                print(f"          - Matched Email query. Email stored: {val!r}")
                return res
            fallback = "I don't know your email yet. You can tell me by saying 'My email is [Email address]'."
            return fallback

    # 7. Check for History queries (e.g. "tell me the last 5 conversations")
    history_match = re.search(r"(?:last|past|show)\s*(\d*)\s*(?:conversation|chat|history|message|turn)", message_lower)
    if history_match or "conversation history" in message_lower or "show history" in message_lower or "what was our conversation" in message_lower:
        count = 5
        if history_match and history_match.group(1):
            try:
                count = int(history_match.group(1))
            except ValueError:
                pass
                
        history = session.get("history", [])
        if not history:
            res = "We haven't started a conversation history yet!"
            return res
            
        recent_history = history[-count:]
        lines = []
        for item in recent_history:
            speaker = "User" if item["role"] == "user" else "Chatbot"
            lines.append(f"- {speaker}: {item['message']}")
            
        formatted_history = "\n".join(lines)
        res = f"Here are the last {len(recent_history)} messages of our conversation:\n{formatted_history}"
        return res

    print("          - Message is not a context query.")
    return None


# =====================================================================
# save_context Function
# =====================================================================
def save_context(extracted_entities: dict, user_id: str = "default_user") -> Optional[str]:
    """
    Why it exists:
        Saves already extracted entities into the user's session,
        and returns an acknowledgement string if a key state variable changed.
    """
    print(f"      ▶ [context.py:save_context] Called with extracted_entities={extracted_entities!r}, user_id={user_id!r}")
    session = get_session(user_id)
    
    # Track old states to check for updates
    old_states = {k: session.get(k) for k in [
        "applicant_name", "loan_type", "loan_amount", "monthly_income", 
        "employment_type", "occupation", "employer_name", "loan_tenure", 
        "property_value", "application_id", "email", "phone_number", 
        "pan_number", "aadhaar_number"
    ]}
    
    # Save entities
    if "applicant_name" in extracted_entities:
        session["applicant_name"] = extracted_entities["applicant_name"]
        session["name"] = extracted_entities["applicant_name"]
    if "loan_type" in extracted_entities:
        session["loan_type"] = extracted_entities["loan_type"]
        session["product"] = extracted_entities["loan_type"]
    if "loan_amount" in extracted_entities:
        session["loan_amount"] = extracted_entities["loan_amount"]
        session["amount"] = extracted_entities["loan_amount"]
    if "monthly_income" in extracted_entities:
        session["monthly_income"] = extracted_entities["monthly_income"]
    if "employment_type" in extracted_entities:
        session["employment_type"] = extracted_entities["employment_type"]
    if "occupation" in extracted_entities:
        session["occupation"] = extracted_entities["occupation"]
    if "employer_name" in extracted_entities:
        session["employer_name"] = extracted_entities["employer_name"]
    if "loan_tenure" in extracted_entities:
        session["loan_tenure"] = extracted_entities["loan_tenure"]
    if "property_value" in extracted_entities:
        session["property_value"] = extracted_entities["property_value"]
    if "application_id" in extracted_entities:
        session["application_id"] = extracted_entities["application_id"]
    if "email" in extracted_entities:
        session["email"] = extracted_entities["email"]
    if "phone_number" in extracted_entities:
        session["phone_number"] = extracted_entities["phone_number"]
        session["phone"] = extracted_entities["phone_number"]
    if "pan_number" in extracted_entities:
        session["pan_number"] = extracted_entities["pan_number"]
    if "aadhaar_number" in extracted_entities:
        session["aadhaar_number"] = extracted_entities["aadhaar_number"]

    # Generate Acknowledgement responses for updates
    if session["applicant_name"] != old_states["applicant_name"]:
        ack = f"Nice to meet you, {session['applicant_name']}! I've saved your name."
        print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
        return ack
    if session["loan_type"] != old_states["loan_type"]:
        ack = f"Got it! I've noted that you selected a {session['loan_type']} Loan."
        print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
        return ack
    if session["monthly_income"] != old_states["monthly_income"]:
        ack = f"Got it! I've saved your monthly income as ₹{session['monthly_income']}."
        print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
        return ack
    if session["loan_amount"] != old_states["loan_amount"]:
        ack = f"Got it! I've saved your requested loan amount as {session['loan_amount']}."
        print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
        return ack
    if session["employment_type"] != old_states["employment_type"]:
        ack = f"Got it! I've saved your employment type as {session['employment_type']}."
        print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
        return ack
        
    # Support other simple updates
    for key in ["pan_number", "aadhaar_number", "phone_number", "email", "occupation", "employer_name", "loan_tenure", "property_value", "application_id"]:
        if session.get(key) != old_states.get(key):
            ack = f"Thank you! I have saved your {key.replace('_', ' ')} as {session[key]}."
            print(f"      ◀ [context.py:save_context] Returning Acknowledgement: {ack!r}")
            return ack
            
    print("        - No state variables updated.")
    print("      ◀ [context.py:save_context] Returning: None")
    return None


# =====================================================================
# retrieve_context Function
# =====================================================================
def retrieve_context(message: str, user_id: str = "default_user") -> Optional[str]:
    """
    Why it exists:
        Checks if the user is asking about previously stored information
        (e.g., 'What is my name?'). If so, returns the stored details.
    """
    print(f"      ▶ [context.py:retrieve_context] Called with message={message!r}, user_id={user_id!r}")
    query_reply = handle_context_query(message, user_id)
    if query_reply is not None:
        print(f"        - Context query matched.")
        print(f"      ◀ [context.py:retrieve_context] Returning: {query_reply!r}")
        return query_reply
    print(f"        - Not a context query.")
    print(f"      ◀ [context.py:retrieve_context] Returning: None")
    return None


# =====================================================================
# process_context Function (Backward Compatibility Wrapper)
# =====================================================================
def process_context(message: str, user_id: str = "default_user") -> Optional[str]:
    """
    Why it exists:
        Orchestrates saving and retrieving in a single step for backward compatibility.
    """
    print(f"      ▶ [context.py:process_context] Called with message={message!r}, user_id={user_id!r}")
    from entity import extract_entities
    extracted = extract_entities(message)
    save_reply = save_context(extracted, user_id)
    if save_reply is not None:
        return save_reply
    return retrieve_context(message, user_id)
