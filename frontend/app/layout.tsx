import React from "react";
import "./globals.css";

// =====================================================================
// RootLayout Component
// =====================================================================
/**
 * Why it exists:
 *   Next.js App Router requires a root layout file to wrap all pages.
 *   This file defines the HTML document structure and base styling.
 */
export const metadata = {
  title: "FastPath Chatbot",
  description: "A simple educational chatbot built with Next.js and FastAPI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <html lang="en" style={{ height: "100%" }}>
      <body style={{ margin: 0, padding: 0, height: "100%", backgroundColor: "#11111b" }}>
        {children}
      </body>
    </html>
  );
}  
