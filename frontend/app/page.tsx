"use client";

import React, { useState } from "react";
import ChatWindow, { Message } from "./ChatWindow";
import ChatInput from "./ChatInput";
import { sendChatMessage } from "./api";

// =====================================================================
// Page Component (Main View)
// =====================================================================
export default function Page(): JSX.Element {
  // Messages history state, starting empty
  const [messages, setMessages] = useState<Message[]>([]);
  
  // Loading state indicating if we are waiting for a backend response
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // =====================================================================
  // handleSendMessage Callback Function
  // =====================================================================
  const handleSendMessage = async (text: string): Promise<void> => {
    // 1. Create a unique ID for the user's message
    const userMessageId = Math.random().toString(36).substring(2, 9);
    
    const userMessage: Message = {
      id: userMessageId,
      sender: "user",
      text: text,
    };

    // 2. Add the user's message to the chat list immediately
    setMessages((prev) => [...prev, userMessage]);
    
    // 3. Enable loading state
    setIsLoading(true);

    try {
      // 4. Send message to the backend via our API utility
      const data = await sendChatMessage(text);

      // 5. Build the chatbot's response object
      const botMessageId = Math.random().toString(36).substring(2, 9);
      const botMessage: Message = {
        id: botMessageId,
        sender: "bot",
        text: data.response,
        detectedType: data.detected_type,
      };

      // 6. Append the bot's response to the message list
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // 7. Error handling: display error message inside the chat
      const errorMessageId = Math.random().toString(36).substring(2, 9);
      const errorMessage: Message = {
        id: errorMessageId,
        sender: "bot",
        text: "Error: Failed to connect to the backend server. Make sure FastAPI is running on port 8000.",
        detectedType: "gibberish", // Mark as red/warning badge
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      // 8. Turn off loading spinner
      setIsLoading(false);
    }
  };

  // -------------------------------------------------------------------
  // Premium Inline Styling Objects (Sleek Dark Mode & Glassmorphism)
  // -------------------------------------------------------------------
  const mainStyle: React.CSSProperties = {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "radial-gradient(circle at top left, #1e1e2e 0%, #11111b 100%)",
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    padding: "20px",
    boxSizing: "border-box",
  };

  const containerStyle: React.CSSProperties = {
    width: "100%",
    maxWidth: "700px",
    height: "80vh",
    minHeight: "550px",
    maxHeight: "800px",
    display: "flex",
    flexDirection: "column",
    borderRadius: "24px",
    overflow: "hidden",
    background: "rgba(24, 24, 37, 0.45)",
    backdropFilter: "blur(20px)",
    border: "1px solid rgba(255, 255, 255, 0.08)",
    boxShadow: "0 20px 50px rgba(0, 0, 0, 0.4)",
  };

  const headerStyle: React.CSSProperties = {
    padding: "20px 24px",
    background: "rgba(30, 30, 46, 0.5)",
    borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  };

  const titleStyle: React.CSSProperties = {
    margin: 0,
    fontSize: "20px",
    fontWeight: "bold",
    background: "linear-gradient(135deg, #cba6f7 0%, #89b4fa 100%)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  };

  const subtitleStyle: React.CSSProperties = {
    margin: 0,
    fontSize: "12px",
    color: "#a6adc8",
    letterSpacing: "0.5px",
  };

  return (
    <main style={mainStyle}>
      <div style={containerStyle}>
        {/* Chatbot App Header */}
        <header style={headerStyle}>
          <h1 style={titleStyle}>Loan Origination System Chatbot</h1>
          <p style={subtitleStyle}>Rule-based LOS Pipeline • Modules 1–8 Educational Sandbox</p>
        </header>

        {/* Scrollable Conversation Window */}
        <ChatWindow messages={messages} isLoading={isLoading} />

        {/* Input Text Form */}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </main>
  );
}
