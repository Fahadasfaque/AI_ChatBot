import React, { useEffect, useRef } from "react";

// =====================================================================
// Message and ChatWindowProps Interfaces
// =====================================================================
export interface Message {
  id: string;
  sender: "user" | "bot";
  text: string;
  detectedType?: string; // Metadata from the backend (greeting, gibberish, echo)
}

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

// =====================================================================
// ChatWindow Component
// =====================================================================
export default function ChatWindow({ messages, isLoading }: ChatWindowProps): JSX.Element {
  // Reference to the dummy div at the bottom of the list for auto-scrolling
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll effect: run whenever the messages array or loading state changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // -------------------------------------------------------------------
  // Premium Inline Styling Objects
  // -------------------------------------------------------------------
  const windowStyle: React.CSSProperties = {
    flex: 1,
    padding: "24px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    background: "rgba(17, 17, 27, 0.6)",
  };

  const emptyStateStyle: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100%",
    color: "#7f849c",
    textAlign: "center",
    gap: "8px",
  };

  const messageRowStyle = (sender: "user" | "bot"): React.CSSProperties => ({
    display: "flex",
    justifyContent: sender === "user" ? "flex-end" : "flex-start",
    width: "100%",
  });

  const bubbleStyle = (sender: "user" | "bot"): React.CSSProperties => ({
    maxWidth: "70%",
    padding: "12px 18px",
    borderRadius: "16px",
    borderTopRightRadius: sender === "user" ? "4px" : "16px",
    borderTopLeftRadius: sender === "bot" ? "4px" : "16px",
    lineHeight: "1.5",
    fontSize: "15px",
    color: sender === "user" ? "#11111b" : "#cdd6f4",
    background: sender === "user"
      ? "linear-gradient(135deg, #89b4fa 0%, #b4befe 100%)"
      : "rgba(255, 255, 255, 0.05)",
    border: sender === "bot" ? "1px solid rgba(255, 255, 255, 0.1)" : "none",
    boxShadow: sender === "user" 
      ? "0 4px 15px rgba(137, 180, 250, 0.2)" 
      : "none",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  });

  const badgeStyle = (type?: string): React.CSSProperties => {
    let color = "#a6e3a1"; // Green for greeting
    if (type === "gibberish") color = "#f38ba8"; // Red for gibberish
    if (type === "echo") color = "#cba6f7"; // Purple for echo

    return {
      fontSize: "10px",
      fontWeight: "bold",
      textTransform: "uppercase",
      letterSpacing: "0.5px",
      color: color,
      marginTop: "4px",
      alignSelf: "flex-start",
    };
  };

  const loadingBubbleStyle: React.CSSProperties = {
    display: "flex",
    gap: "4px",
    padding: "12px 18px",
    borderRadius: "16px",
    borderTopLeftRadius: "4px",
    background: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    alignSelf: "flex-start",
  };

  return (
    <div style={windowStyle}>
      {messages.length === 0 ? (
        <div style={emptyStateStyle}>
          <h3 style={{ margin: 0, color: "#bac2de" }}>Start a Conversation</h3>
          <p style={{ margin: 0, fontSize: "14px" }}>Say hi or ask a question to trigger the LOS pipeline.</p>
        </div>
      ) : (
        messages.map((msg) => (
          <div key={msg.id} style={messageRowStyle(msg.sender)}>
            <div style={bubbleStyle(msg.sender)}>
              <div>{msg.text}</div>
              {msg.sender === "bot" && msg.detectedType && (
                <span style={badgeStyle(msg.detectedType)}>
                  Intent: {msg.detectedType}
                </span>
              )}
            </div>
          </div>
        ))
      )}

      {isLoading && (
        <div style={loadingBubbleStyle}>
          <span style={{ color: "#7f849c", fontSize: "14px" }}>typing...</span>
        </div>
      )}

      {/* Dummy div to scroll to */}
      <div ref={bottomRef} />
    </div>
  );
}
