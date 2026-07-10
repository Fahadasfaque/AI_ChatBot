# backend/greeting.py
"""
Purpose:
    This file contains the logic for detecting whether a user's message is a greeting
    and generating an appropriate greeting response.

Why this file exists:
    Greeting detection is a standard feature that helps start conversations.
    By identifying pure greetings immediately, we can respond instantly without
    running intent classification.

How it works:
    We use Regular Expressions (Regex) to match common greeting patterns:
    1. Greeting Root: Matches common words (e.g., "hi", "hello", "hey", "good morning").
       It supports character elongation like "hiii" or "hellooo".
    2. Conversational Padding: Optionally matches simple pronouns/additions (e.g., "there", "bot", "friend").
    3. Trailing Punctuation: Ignores punctuation marks like "!", ".", or "?".
    
    This regex is designed to only match PURE greetings (e.g. "hi there!").
    If the message contains a greeting followed by actual intent (e.g. "hi, I need support"),
    the regex will NOT match, allowing it to fall through to Intent Detection.

Input:
    message (str): The raw text message sent by the user.

Output:
    bool: True if the message is a pure greeting, False otherwise.
"""

import re



# Compiled regex pattern for pure greeting validation.
# Structure:
# ^(hi+|hello+|hey+|yo+|hola+|hlw+|good\s*(morning|afternoon|evening|day)) -> Matches starting greeting word (with letter elongation support).
# (\s+(there|bot|friend|assistant|buddy|bro|all|everyone))? -> Matches optional address padding.
# [!.,?]*$ -> Matches optional trailing punctuation up to the end of the string.
CORE_GREETINGS = r"(hi+|hello+|hey+|yo+|hola+|hlw+|hiya+|sup+|bonjour+|namaste+|greetings+|gm+|gn)"
TIME_GREETINGS = r"(good\s*(morning|afternoon|evening|day|night))"
ADDRESS_PADDING = r"(\s+(there|bot|friend|assistant|buddy|bro|all|everyone))?"

GREETING_PATTERN = re.compile(
    rf"^({CORE_GREETINGS}|{TIME_GREETINGS}){ADDRESS_PADDING}[!.,?]*$",
    re.IGNORECASE
)

# Compiled regex pattern to check if a message starts with a greeting (even if followed by other text).
GREETING_START_PATTERN = re.compile(
    rf"^({CORE_GREETINGS}|{TIME_GREETINGS})\b",
    re.IGNORECASE
)

# Dictionary lookup of greeting responses to avoid long if-elif chains.
# Using python's format placeholder {name} to support personalization.
GREETING_RESPONSES = {
    "hi": "Hi{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "hello": "Hello{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "hey": "Hey there{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "hlw": "Hello{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "hiya": "Hiya{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "yo": "Yo! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "sup": "Not much! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "bonjour": "Bonjour{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "namaste": "Namaste{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "greetings": "Greetings{name}. Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "hola": "¡Hola{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "good morning": "Good morning{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "good afternoon": "Good afternoon{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "good evening": "Good evening{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "good night": "Good night{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "good day": "Good day{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "gm": "Good morning{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status",
    "gn": "Good night{name}! Welcome to the Loan Origination System. I can help you with:\n• Loan Products\n• Eligibility\n• Documents\n• EMI\n• Interest Rates\n• Application Status"
}


# =====================================================================
# is_greeting Function
# =====================================================================
def is_greeting(message: str) -> bool:
    """
    Why it exists:
        Determines if the incoming message is a pure greeting.
        It uses a regex pattern to safely identify greetings without hijacking
        actual user intents.

    What it receives:
        message (str): The raw text message sent by the user.

    What it returns:
        bool: True if the message matches a greeting pattern, False otherwise.
    """
    print(f"        ▶ [greeting.py:is_greeting] Called with message={message!r}")
    cleaned = message.strip()
    result = bool(GREETING_PATTERN.match(cleaned))
    print(f"        ◀ [greeting.py:is_greeting] Returning result={result}")
    return result


# =====================================================================
# starts_with_greeting Function
# =====================================================================
def starts_with_greeting(message: str) -> bool:
    """
    Why it exists:
        Checks if the message starts with any greeting root word.
        This allows identifying greetings when mixed with names or extra text.

    What it receives:
        message (str): The raw text message sent by the user.

    What it returns:
        bool: True if the message starts with a greeting pattern, False otherwise.
    """
    print(f"        ▶ [greeting.py:starts_with_greeting] Called with message={message!r}")
    cleaned = message.strip()
    result = bool(GREETING_START_PATTERN.match(cleaned))
    print(f"        ◀ [greeting.py:starts_with_greeting] Returning result={result}")
    return result


# =====================================================================
# get_greeting_response Function
# =====================================================================
def get_greeting_response(message: str, name: str = None) -> str:
    """
    Why it exists:
        This function returns a friendly, personalized greeting response
        based on the specific greeting type used by the user.

    What it receives:
        message (str): The raw text message sent by the user.
        name (str, optional): The name of the user to personalize the greeting.

    What it returns:
        str: A specific greeting reply matching the greeting root word.
    """
    print(f"        ▶ [greeting.py:get_greeting_response] Called with message={message!r}, name={name!r}")
    cleaned = message.strip()
    
    # 1. Try pure greeting match first
    match = GREETING_PATTERN.match(cleaned)
    if not match:
        # Fallback to start-of-message greeting match
        match = GREETING_START_PATTERN.match(cleaned)
        
    name_str = f" {name}" if name else ""

    if not match:
        result = f"Hello{name_str}! How can I help you?"
        print(f"        ◀ [greeting.py:get_greeting_response] No regex match. Returning fallback: {result!r}")
        return result

    # 2. Extract the root greeting (group 1 of the regex match) and normalize spaces
    root_greeting = re.sub(r"\s+", " ", match.group(1).lower())

    # 3. Dynamic lookup mapping of greetings
    # Sort keys by length descending to match the longest greeting key first (e.g., "good morning" before "good")
    for key, response in sorted(GREETING_RESPONSES.items(), key=lambda x: len(x[0]), reverse=True):
        if root_greeting.startswith(key):
            result = response.format(name=name_str)
            print(f"        - Matched greeting key: {key!r}")
            print(f"        ◀ [greeting.py:get_greeting_response] Returning: {result!r}")
            return result

    # 4. Fallback greeting
    result = GREETING_RESPONSES["hello"].format(name=name_str)
    print(f"        ◀ [greeting.py:get_greeting_response] Returning default fallback hello: {result!r}")
    return result
