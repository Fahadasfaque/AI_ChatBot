/**
 * frontend/app/api.ts
 * 
 * This file handles communicating with our FastAPI backend.
 * It defines TypeScript interfaces matching the backend's Pydantic schemas,
 * and contains the fetch logic to send messages to the server.
 */

// =====================================================================
// TypeScript Interfaces (Data Models)
// =====================================================================

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  detected_type: string;
}

// Default base URL for the FastAPI backend.
// In local development, FastAPI runs on port 8000 by default.
const BASE_URL = "http://127.0.0.1:8000";

// =====================================================================
// sendChatMessage Function
// =====================================================================
export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const requestBody: ChatRequest = { message };
  console.log(requestBody)

  // Make the network request to the backend chat API
  const response = await fetch(`${BASE_URL}/api/conversation`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });
  console.log(response);


  // If the HTTP status is not ok (200-299), throw an error
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  // Parse and return the JSON response from the backend
  const data: ChatResponse = await response.json();
  console.log(data)
  return data;
  
}
