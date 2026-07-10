import React, { useState, FormEvent, ChangeEvent, useRef, useEffect } from "react";

// =====================================================================
// ChatInputProps Interface
// =====================================================================
interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

// =====================================================================
// ChatInput Component
// =====================================================================
export default function ChatInput({ onSendMessage, isLoading }: ChatInputProps): JSX.Element {
  // Local state to store the current text typed in the input box
  const [text, setText] = useState<string>("");

  // Ref to target the input element for refocusing
  const inputRef = useRef<HTMLInputElement>(null);

  // Handler for text input changes
  const handleTextChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setText(e.target.value);
  };

  // Handler for form submission
  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    
    // Only send the message if it's not empty/spaces and not currently loading
    if (text.trim() && !isLoading) {
      onSendMessage(text.trim());
      setText(""); // Clear the input field after sending
    }
  };

  // Keep focus on the input box automatically when loading finishes
  useEffect(() => {
    if (!isLoading) {
      inputRef.current?.focus();
    }
  }, [isLoading]);


  // -------------------------------------------------------------------
  // Premium Inline Styling Objects
  // -------------------------------------------------------------------
  const formStyle: React.CSSProperties = {
    display: "flex",
    gap: "12px",
    width: "100%",
    padding: "16px",
    background: "rgba(30, 30, 46, 0.4)",
    backdropFilter: "blur(12px)",
    borderTop: "1px solid rgba(255, 255, 255, 0.1)",
    boxSizing: "border-box",
  };

  const inputStyle: React.CSSProperties = {
    flex: 1,
    padding: "14px 20px",
    borderRadius: "12px",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    background: "rgba(255, 255, 255, 0.05)",
    color: "#cdd6f4",
    fontSize: "15px",
    outline: "none",
    transition: "all 0.2s ease-in-out",
  };

  const buttonStyle: React.CSSProperties = {
    padding: "0 24px",
    borderRadius: "12px",
    border: "none",
    background: isLoading 
      ? "rgba(255, 255, 255, 0.1)" 
      : "linear-gradient(135deg, #89b4fa 0%, #b4befe 100%)",
    color: isLoading ? "#7f849c" : "#11111b",
    fontSize: "15px",
    fontWeight: "bold",
    cursor: isLoading ? "not-allowed" : "pointer",
    transition: "all 0.2s ease",
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <input
        ref={inputRef}
        type="text"
        value={text}
        onChange={handleTextChange}
        disabled={isLoading}
        placeholder={isLoading ? "Chatbot is thinking..." : "Ask about loans, documents, or apply..."}
        style={inputStyle}
      />
      <button 
        type="submit" 
        disabled={isLoading || !text.trim()} 
        style={buttonStyle}
      >
        {isLoading ? "..." : "Send"}
      </button>
    </form>
  );
}
