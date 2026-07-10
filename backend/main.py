# backend/main.py
"""
This is the main entry point of our FastAPI application.
It initializes the FastAPI app, configures Cross-Origin Resource Sharing (CORS)
so the Next.js frontend can communicate with it, and exposes the HTTP endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatMessageRequest, ChatMessageResponse
from chat import handle_chat_message

# Create the FastAPI application instance
app = FastAPI(title="Simple Chatbot API")

# Configure CORS (Cross-Origin Resource Sharing).
# This is required because our Next.js frontend will run on a different port 
# (e.g. http://localhost:3000) than our FastAPI backend (e.g. http://localhost:8000).
# Without this, the browser would block requests from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local educational development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)


# =====================================================================
# GET / Route (Health Check)
# =====================================================================
@app.get("/")
def read_root() -> dict:
    """
    Why it exists:
        A simple root route to verify that the backend server is running 
        and healthy.

    Input:
        None

    Output:
        dict: A simple JSON message confirming the API is active.
    """
    return {"status": "ok", "message": "Simple Chatbot API is running"}


# =====================================================================
# POST /api/chat Route (Chat Endpoint)
# =====================================================================
@app.post("/api/conversation", response_model=ChatMessageResponse)
def chat_endpoint(request: ChatMessageRequest) -> ChatMessageResponse:
    """
    Why it exists:
        This is the main endpoint that the frontend calls when a user
        sends a chat message. It receives the user message and returns
        the bot response.
    Input:
        request (ChatMessageRequest): Pydantic model validating that the 
                                      incoming JSON contains a "message" field.

    Output:
        ChatMessageResponse: Pydantic model validating that the response
                             contains the "response" text and "detected_type".
    """
    # Delegate the request handling to the chat logic module
    print(f"\n▶ [main.py:chat_endpoint] Called with request.message={request.message!r}")
    response = handle_chat_message(request)
    print(f"◀ [main.py:chat_endpoint] Returning response={response!r}\n")
    return response
