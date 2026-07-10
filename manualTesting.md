# Chatbot Manual Verification Test Suite

This document lists the recommended test cases to verify all modules of the chatbot pipeline, with a focus on the **Search and Ranking Engine** (Module 7).

## How to Test

1. Start the FastAPI backend (it will automatically reload on edits):
   ```bash
   .venv\Scripts\uvicorn.exe main:app --port 8000 --reload
   ```
2. Interact with the chat interface in your browser or send POST requests to `http://127.0.0.1:8000/api/chat` with JSON body:
   ```json
   {
     "message": "<User Input>"
   }
   ```

---

## Test Cases

| No. | Test Message (Input) | Pipeline Route / Logic Path | Expected Response |
| :--- | :--- | :--- | :--- |
| **1** | `hello there!` | **FastPath** → greeting matches | `Hello! How can I help you today?` (Returns early without intent/search processing) |
| **2** | `asdfghjkl` | **FastPath** → consonant cluster matches | A randomly selected warning (e.g., `I'm unable to process that request. Could you clarify?`) |
| **3** | `What is chatbot pricing?` | **Search Engine** → matches `"chatbot pricing..."` candidate (Score: 33.3% $\ge 30\%$) | `Our chatbot starts from ₹999/month.` |
| **4** | `Chatbot subscription` | **Search Engine** → matches `"chatbot pricing..."` candidate (Score: 33.3% $\ge 30\%$) | `Our chatbot starts from ₹999/month.` |
| **5** | `What are your business hours?` | **Search Engine** → matches `"business hours"` candidate (Score: 100% $\ge 30\%$) | `Monday to Friday 9AM to 6PM` |
| **6** | `Where is your office located?` | **Search Engine** → matches `"support contact address..."` candidate (Score: 33.3% $\ge 30\%$) | `ABC Technologies, Connaught Place, New Delhi` |
| **7** | `where is company?` | **Search Engine** → matches `"company location..."` candidate (Score: 40.0% $\ge 30\%$) | `ABC Technologies is located in Delhi.` |
| **8** | `When was the company founded?` | **Search Engine** → matches `"company founded..."` candidate (Score: 33.3% $\ge 30\%$) | `ABC Technologies was founded in 2020.` |
| **9** | `my name is Kamlesh` | **Context** → extracts name, saves context, returns acknowledgement | `Nice to meet you, Kamlesh! I've saved your name.` |
| **10** | `what is my name?` | **Context** → queries context from session | `Your name is Kamlesh.` |
| **11** | `tell me a joke` | **Search Engine** → no candidate matches above 30.0% $\rightarrow$ falls back to random reply | A randomly selected fallback (e.g., `That topic is currently outside of my capabilities.`) |
| **12** | `thanks` | **Intent** (thank_you) → bypasses Search Engine | A randomly selected appreciation response (e.g., `Happy to help. Is there anything else I can assist you with today?`) |
| **13** | `my email is fahadasfaque@gmail.com` | **Context** → extracts email, saves context, returns acknowledgement | `Got it! I've noted that your email is fahadasfaque@gmail.com.` |
| **14** | `what is my email?` | **Context** → queries email context from session | `Your email is fahadasfaque@gmail.com.` |
| **15** | `good morniing` | **Spelling Correction** $\rightarrow$ corrected to `good morning` $\rightarrow$ **FastPath** greeting | `Good morning! Hope your day is off to a great start.` |
| **16** | `coost of chatbot` | **Spelling Correction** $\rightarrow$ corrected to `cost of chatbot` $\rightarrow$ **Search Engine** (Score: 33.3% $\ge 30\%$) | `Our chatbot starts from ₹999/month.` |
| **17** | `TELL ME THE LAST 5 CONVERSATION` | **Context** $\rightarrow$ retrieves and formats the last 5 messages from session history | A formatted list of the last 5 messages in chronological order. |





