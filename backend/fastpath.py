# backend/fastpath.py
"""
This file implements the FastPath logic of our chatbot.
FastPath acts as a simple router that processes messages using quick rule checks
rather than complex AI models. It executes checks in a sequential order:
1. Is it a greeting? -> Return greeting response.
2. Is it gibberish? -> Return gibberish warning.
3. Otherwise -> Echo the original message back.
"""

# Import the detection and response functions we created earlier
from greeting import is_greeting, get_greeting_response
from gibberish import is_gibberish, get_gibberish_response


# =====================================================================
# process_fastpath Function
# =====================================================================
def process_fastpath(message: str) -> tuple[str, str]:
    """
    Why it exists:
        This function handles the decision-making (routing) for the incoming message.
        It runs the FastPath rules sequentially and returns the appropriate response
        along with the type of message detected.

    Input:
        message (str): The raw text message sent by the user.

    Output:
        tuple[str, str]: A tuple containing:
            1. The response string for the user.
            2. The type of message detected ("greeting", "gibberish", or "echo").
    """
    print(f"      ▶ [fastpath.py:process_fastpath] Called with message={message!r}")
    
    # Step 1: Check if the message is a Greeting
    print(f"        - Running is_greeting() check...")
    if is_greeting(message):
        response_text = get_greeting_response(message)
        print(f"        - is_greeting matched! Generating greeting response...")
        print(f"      ◀ [fastpath.py:process_fastpath] Returning Greeting: (response_text={response_text!r}, detected_type='greeting')")
        return response_text, "greeting"
        
    # Step 2: Check if the message is Gibberish
    print(f"        - Running is_gibberish() check...")
    if is_gibberish(message):
        response_text = get_gibberish_response()
        print(f"        - is_gibberish matched! Generating gibberish response...")
        print(f"      ◀ [fastpath.py:process_fastpath] Returning Gibberish: (response_text={response_text!r}, detected_type='gibberish')")
        return response_text, "gibberish"
        
    # Step 3: Default fallback - Echo the message back to the user
    print(f"        - No early FastPath match. Defaulting to 'echo'...")
    response_text = message
    detected_type = "echo"
    print(f"      ◀ [fastpath.py:process_fastpath] Returning Fallback: (response_text={response_text!r}, detected_type='echo')")
    return response_text, detected_type