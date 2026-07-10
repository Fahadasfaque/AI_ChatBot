# backend/chat.py
"""
This file handles the chat request logic.
It acts as the mediator between the incoming API requests (which use Pydantic models)
and the core chatbot coordinator logic. By wrapping the response in the Pydantic
response schema here, we keep the main API routes in main.py clean.
"""

from schemas import ChatMessageRequest, ChatMessageResponse
from chatbot import get_bot_response


# =====================================================================
# handle_chat_message Function
# =====================================================================
def handle_chat_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """
    Why it exists:
        This function receives the validated request from the API layer,
        extracts the message, gets the bot's response, and structures the
        result into the defined ChatMessageResponse Pydantic schema.

    Input:
        request (ChatMessageRequest): Validated request containing the user's message.

    Output:
        ChatMessageResponse: Structured response model ready to be returned as JSON.
    """
    print(f"  ▶ [chat.py:handle_chat_message] Called with request.message={request.message!r}")
    
    # 1. Extract the raw text message from the request object
    user_message = request.message
    
    # 2. Get response details from the chatbot coordinator
    reply, detected_type, score = get_bot_response(user_message)
    
    # 3. Build and return the structured response object
    response = ChatMessageResponse(
        response=reply,
        detected_type=detected_type,
        score=score
    )
    print(f"  ◀ [chat.py:handle_chat_message] Returning ChatMessageResponse(response={reply!r}, detected_type={detected_type!r}, score={score!r})")
    return response
