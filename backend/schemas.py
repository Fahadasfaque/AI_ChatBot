# backend/schemas.py
"""
This file defines the data structures (schemas) used by our FastAPI backend.
We use Pydantic models to validate the incoming and outgoing data, ensuring
that both the frontend and backend agree on the format of messages.
"""

from pydantic import BaseModel

# =====================================================================
# ChatMessageRequest Schema
# =====================================================================
class ChatMessageRequest(BaseModel):
    """
    Why it exists:
        This class represents the structure of the data sent by the user
        from the Next.js frontend to the FastAPI backend. It ensures the 
        request contains a valid message field.

    Input (Attributes):
        message (str): The text message sent by the user (e.g., "Hello", "asdfghjk").
    """
    message: str
 

from typing import Optional

# =====================================================================
# ChatMessageResponse Schema
# =====================================================================
class ChatMessageResponse(BaseModel):
    """
    Why it exists:
        This class represents the structure of the data returned by the 
        backend back to the frontend. It includes both the bot's text reply 
        and metadata about how the message was categorized.

    Output (Attributes):
        response (str): The reply message from the chatbot (e.g., "Hello! How can I help you?").
        detected_type (str): The routing path taken by the FastPath logic (e.g., "greeting", "gibberish", "echo").
        score (Optional[float]): The similarity score calculated by the search engine, if applicable.
    """
    response: str
    detected_type: str
    score: Optional[float] = None
