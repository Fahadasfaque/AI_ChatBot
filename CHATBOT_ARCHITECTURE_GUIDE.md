# Chatbot Architecture Study Guide

This document is a comprehensive, step-by-step technical study guide of our rule-based chatbot codebase. It serves as your personal reference for code reviews, architectural audits, and software engineering alignment meetings.

---

## 1. System Architecture Overview

Our application is built as a modular, rule-based chatbot utilizing a **Pipes-and-Filters pipeline design**. The architecture is entirely deterministic, avoiding heavy machine learning models in production to ensure high predictability, low latency, and zero dependency on external network APIs. 

### Folder Structure
```text
chatbot/
├── backend/
│   ├── knowledge/               # Static Knowledge Base JSON files
│   │   ├── company.json
│   │   ├── faq.json
│   │   ├── pricing.json
│   │   ├── products.json
│   │   └── support.json
│   ├── chat.py                  # API Controller/Mediator
│   ├── chatbot.py               # Central Pipeline Coordinator
│   ├── context.py               # Context Memory Manager
│   ├── embedding_demo.py        # Conceptual Vector Search Study File (Independent)
│   ├── entity.py                # Regex-based Entity Extractor
│   ├── fastpath.py              # Rule-based Router (Greetings/Gibberish)
│   ├── gibberish.py             # Pattern-based Gibberish Detector
│   ├── greeting.py              # Regex-based Greeting Handler
│   ├── intent.py                # Keyword-based Intent Classifier
│   ├── knowledge_base.py        # Knowledge Access layer
│   ├── main.py                  # FastAPI Application Entry point
│   ├── requirements.txt         # Production Dependencies
│   ├── response_generator.py    # Output compiler/formatter
│   ├── schemas.py               # Pydantic Request/Response models
│   └── search_engine.py         # Set overlap and fuzzy matching Search Engine
├── frontend/                    # Next.js Frontend Application
└── CHATBOT_ARCHITECTURE_GUIDE.md # This guide
```

---

## 2. Complete Request Flow

When a user types a message and clicks "Send", the request travels through the following path:

```
[User Input]
     ↓
[Frontend: App Interface] 
     ↓ (HTTP POST to /api/conversation)
[FastAPI: main.py] 
     ↓ (Validates payload against ChatMessageRequest schema)
[Controller: chat.py] 
     ↓ (Calls get_bot_response)
[Coordinator: chatbot.py]
     ↓ (Step 0: search_engine.correct_spelling)
[Spelling Corrector] 
     ↓ (Step 1: process_fastpath)
[FastPath Router] ─── (Matches Greeting or Gibberish) ───► [FastPath Early Return] ──┐
     ↓ (No early match: returns "echo")                                             │
[Intent Detector: intent.py]                                                        │
     ↓ (Classifies intent like 'pricing', 'support')                                │
[Entity Extractor: entity.py]                                                       │
     ↓ (Extracts name, email, phone, amounts, products)                             │
[Context Processor: context.py]                                                     │
     ↓ (Checks name/city/email/loan updates or history query requests)              │
[Knowledge Base: knowledge_base.py]                                                 │
     ↓ (Calls search_engine.search_kb)                                              │
[Search Engine: search_engine.py]                                                   │
     ↓ (Calculates fuzzy token similarity, ranks candidates)                        │
[Response Generator: response_generator.py]                                         │
     ↓ (Compiles final answer, falls back to UNKNOWN handlers if needed)            │
[History Logger: add_to_history] ◄──────────────────────────────────────────────────┘
     ↓ (Saves turn to session memory)
[FastAPI Response]
     ↓ (Formatted as JSON via ChatMessageResponse schema)
[Frontend Renderer] ──► [User View]
```

---

## 3. File Responsibilities

| File Name | Layer | Purpose / Responsibility | Introduced In | Called By | Calls | Separated Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [main.py](file:///c:/Users/Admin/Desktop/chatbot/backend/main.py) | API / Routing | Web Server Entry Point. Boots FastAPI, configures CORS middleware, and exposes HTTP endpoints. | Module 1 | Uvicorn / Web Server | `schemas.py`, `chat.py` | Separates HTTP server settings from application logic. |
| [schemas.py](file:///c:/Users/Admin/Desktop/chatbot/backend/schemas.py) | API / Data Contract | Validates request inputs and formats JSON responses using Pydantic. | Module 1 | `main.py`, `chat.py` | None | Guarantees data type enforcement and documentation. |
| [chat.py](file:///c:/Users/Admin/Desktop/chatbot/backend/chat.py) | Controller | Mediates API endpoints and the chatbot pipeline. Structurizes return values. | Module 1 | `main.py` | `schemas.py`, `chatbot.py` | Decouples HTTP request context from Python logic. |
| [chatbot.py](file:///c:/Users/Admin/Desktop/chatbot/backend/chatbot.py) | Coordinator | Runs the sequential pipeline steps and prints execution logs. | Module 1 | `chat.py` | `fastpath.py`, `intent.py`, `entity.py`, `greeting.py`, `context.py`, `knowledge_base.py`, `response_generator.py`, `search_engine.py` | Acts as the central brain orchestrator of the program. |
| [fastpath.py](file:///c:/Users/Admin/Desktop/chatbot/backend/fastpath.py) | FastPath | Determines if messages require early greeting or gibberish responses. | Module 1 | `chatbot.py` | `greeting.py`, `gibberish.py` | Prevents deep processing of trivial or bad inputs. |
| [greeting.py](file:///c:/Users/Admin/Desktop/chatbot/backend/greeting.py) | FastPath | Detects greetings using Regex and formats greeting responses. | Module 1 | `fastpath.py`, `chatbot.py` | None | Centralizes greeting dictionaries and patterns. |
| [gibberish.py](file:///c:/Users/Admin/Desktop/chatbot/backend/gibberish.py) | FastPath | Checks if input is meaningless using phoneme cluster and keyboard crawl checks. | Module 1 | `fastpath.py` | None | Encapsulates complex text-pattern filters. |
| [intent.py](file:///c:/Users/Admin/Desktop/chatbot/backend/intent.py) | NLP Layer | Classifies the intent of user messages via keyword searches. | Module 2 | `chatbot.py` | None | Maps inputs to predefined intents (Pricing, Support). |
| [entity.py](file:///c:/Users/Admin/Desktop/chatbot/backend/entity.py) | NLP Layer | Extracts structured info (amounts, emails, phone numbers, names). | Module 3 | `chatbot.py` | None | Pulls actionable data out of unstructured query strings. |
| [context.py](file:///c:/Users/Admin/Desktop/chatbot/backend/context.py) | Context Layer | Manages session states, variables, and retrieves chat history. | Module 4 | `chatbot.py` | None | Keeps track of user details over multiple dialogue turns. |
| [knowledge_base.py](file:///c:/Users/Admin/Desktop/chatbot/backend/knowledge_base.py) | Knowledge Base | Caches and queries knowledge JSON documents. | Module 6 | `chatbot.py` | `search_engine.py` | Decouples document I/O from NLP matching logic. |
| [search_engine.py](file:///c:/Users/Admin/Desktop/chatbot/backend/search_engine.py) | Knowledge Base | Performs fuzzy search scoring and query spelling correction using RapidFuzz. | Module 7 | `knowledge_base.py`, `chatbot.py` | None | Encapsulates custom search algorithms. |
| [response_generator.py](file:///c:/Users/Admin/Desktop/chatbot/backend/response_generator.py) | Response Layer | Compiles final user-facing text responses and resolves fallbacks. | Module 5 | `chatbot.py` | None | Keeps output templates and formatting in one place. |
| [embedding_demo.py](file:///c:/Users/Admin/Desktop/chatbot/backend/embedding_demo.py) | Study Sandbox | Educational demonstration of vector spaces and cosine similarity. | Module 8 | None (Standalone) | None | Standalone learning sandbox; not used in main pipeline. |

---

## 4. Function Responsibilities

### main.py
* **`read_root()`**
  * **Purpose**: Health check route.
  * **Input**: None
  * **Output**: `{"status": "ok", "message": "Simple Chatbot API is running"}`
  * **Calling Function**: FastAPI Router
  * **Called Functions**: None

* **`chat_endpoint(request: ChatMessageRequest)`**
  * **Purpose**: Web hook for incoming messages.
  * **Input**: `ChatMessageRequest` model (with `message` field).
  * **Output**: `ChatMessageResponse` model.
  * **Calling Function**: FastAPI Router (via frontend POST request)
  * **Called Functions**: `chat.handle_chat_message(request)`

### chat.py
* **`handle_chat_message(request: ChatMessageRequest)`**
  * **Purpose**: Unwraps JSON request, runs coordinator, and builds Pydantic response.
  * **Input**: `ChatMessageRequest`
  * **Output**: `ChatMessageResponse`
  * **Calling Function**: `main.chat_endpoint`
  * **Called Functions**: `chatbot.get_bot_response`

### chatbot.py
* **`get_bot_response(user_message: str)`**
  * **Purpose**: Central pipelines coordinator.
  * **Input**: `user_message` (str)
  * **Output**: `(response_text, intent_name, score)`
  * **Calling Function**: `chat.handle_chat_message`
  * **Called Functions**: `search_engine.correct_spelling`, `fastpath.process_fastpath`, `intent.detect_intent`, `entity.extract_entities`, `context.process_context`, `knowledge_base.query_knowledge_base`, `response_generator.generate_response`, `context.add_to_history`

### fastpath.py
* **`process_fastpath(message: str)`**
  * **Purpose**: Resolves early rules (Greetings, Gibberish).
  * **Input**: `message` (str)
  * **Output**: `(response_text, detected_type)`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: `greeting.is_greeting`, `greeting.get_greeting_response`, `gibberish.is_gibberish`, `gibberish.get_gibberish_response`

### greeting.py
* **`is_greeting(message: str)`**
  * **Purpose**: Checks if a message is a pure greeting.
  * **Input**: `message` (str)
  * **Output**: `bool`
  * **Calling Function**: `fastpath.process_fastpath`
  * **Called Functions**: None

* **`starts_with_greeting(message: str)`**
  * **Purpose**: Checks if message starts with greeting patterns (for fallback).
  * **Input**: `message` (str)
  * **Output**: `bool`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: None

* **`get_greeting_response(message: str, name: str = None)`**
  * **Purpose**: Formulates greeting response text.
  * **Input**: `message` (str), optional `name` (str)
  * **Output**: `str` (greeting text)
  * **Calling Function**: `fastpath.process_fastpath`, `chatbot.get_bot_response`
  * **Called Functions**: None

### gibberish.py
* **`is_gibberish(message: str)`**
  * **Purpose**: Scans message for symbol floods, consonant piles, and keyboard crawls.
  * **Input**: `message` (str)
  * **Output**: `bool`
  * **Calling Function**: `fastpath.process_fastpath`
  * **Called Functions**: None

* **`get_gibberish_response()`**
  * **Purpose**: Returns a random polite warning for gibberish inputs.
  * **Input**: None
  * **Output**: `str`
  * **Calling Function**: `fastpath.process_fastpath`
  * **Called Functions**: None

### intent.py
* **`detect_intent(message: str)`**
  * **Purpose**: Identifies intent using keyword lookup with bypasses for email/phone updates.
  * **Input**: `message` (str)
  * **Output**: `(intent_name, response_text)`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: None

### entity.py
* **`extract_entities(message: str)`**
  * **Purpose**: Extracts email, phone numbers, amounts, products, and names via regex.
  * **Input**: `message` (str)
  * **Output**: `dict` (extracted key-value pairs)
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: None

### context.py
* **`get_session(user_id: str = "default_user")`**
  * **Purpose**: Initializes or retrieves an in-memory user session.
  * **Input**: `user_id` (str)
  * **Output**: `dict`
  * **Calling Function**: `context.add_to_history`, `context.handle_context_query`, `context.process_context`
  * **Called Functions**: None

* **`add_to_history(role: str, message: str, user_id: str = "default_user")`**
  * **Purpose**: Appends message details to the session log history.
  * **Input**: `role` (str), `message` (str), `user_id` (str)
  * **Output**: None
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: `context.get_session`

* **`handle_context_query(message: str, user_id: str = "default_user")`**
  * **Purpose**: Matches context retrieval requests (including conversation history).
  * **Input**: `message` (str), `user_id` (str)
  * **Output**: `str | None`
  * **Calling Function**: `context.process_context`
  * **Called Functions**: `context.get_session`

* **`process_context(message: str, user_id: str = "default_user")`**
  * **Purpose**: Updates session variable states and resolves context queries.
  * **Input**: `message` (str), `user_id` (str)
  * **Output**: `str | None`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: `context.get_session`, `context.handle_context_query`

### knowledge_base.py
* **`load_knowledge_files()`**
  * **Purpose**: Loads all JSON files in the knowledge/ folder and caches them in memory.
  * **Input**: None
  * **Output**: `dict` (knowledge cache)
  * **Calling Function**: `knowledge_base.query_knowledge_base`
  * **Called Functions**: None

* **`query_knowledge_base(query: str, intent_name: str, entities: dict)`**
  * **Purpose**: Searches database using `search_engine` and returns matches $\ge 30\%$ similarity score.
  * **Input**: `query` (str), `intent_name` (str), `entities` (dict)
  * **Output**: `(answer_str, similarity_score)` or `(None, None)`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: `knowledge_base.load_knowledge_files`, `search_engine.search_kb`

### search_engine.py
* **`correct_spelling(message: str)`**
  * **Purpose**: Corrects typos in user query against system vocabulary using RapidFuzz.
  * **Input**: `message` (str)
  * **Output**: `str` (corrected message)
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: None

* **`clean_and_tokenize(text: str)`**
  * **Purpose**: Normalizes, strips punctuation, and splits text into lowercase words.
  * **Input**: `text` (str)
  * **Output**: `set[str]` (set of lowercase word tokens)
  * **Calling Function**: `search_engine.search_kb`
  * **Called Functions**: None

* **`calculate_similarity_score(query_tokens: set[str], candidate_tokens: set[str])`**
  * **Purpose**: Measures similarity score between query tokens and candidate tokens using RapidFuzz character ratios.
  * **Input**: `query_tokens` (set[str]), `candidate_tokens` (set[str])
  * **Output**: `float` (similarity score percentage)
  * **Calling Function**: `search_engine.search_kb`
  * **Called Functions**: None

* **`build_search_candidates(kb: dict)`**
  * **Purpose**: Flattens nested JSON database dictionaries into simple `(question, answer, source)` list objects.
  * **Input**: `kb` (dict)
  * **Output**: `list[dict]`
  * **Calling Function**: `search_engine.search_kb`
  * **Called Functions**: None

* **`search_kb(query: str, kb: dict)`**
  * **Purpose**: Finds the candidate question matching the query with the highest similarity score.
  * **Input**: `query` (str), `kb` (dict)
  * **Output**: `(answer_text, score, source_file)` or `None`
  * **Calling Function**: `knowledge_base.query_knowledge_base`
  * **Called Functions**: `search_engine.clean_and_tokenize`, `search_engine.build_search_candidates`, `search_engine.calculate_similarity_score`

### response_generator.py
* **`generate_response(intent_name, intent_reply, entities, context_reply, kb_reply)`**
  * **Purpose**: Formulates final user response text using intent, entities, context, and knowledge base details.
  * **Input**: `intent_name` (str), `intent_reply` (str), `entities` (dict), `context_reply` (str | None), `kb_reply` (str | None)
  * **Output**: `(final_text, updated_intent_name)`
  * **Calling Function**: `chatbot.get_bot_response`
  * **Called Functions**: None

### embedding_demo.py
* **`dot_product(v1: list[float], v2: list[float])`**
  * **Purpose**: Computes dot product of two vectors.
  * **Input**: two lists of floats.
  * **Output**: `float`
  * **Calling Function**: `embedding_demo.cosine_similarity`
  * **Called Functions**: None

* **`magnitude(v: list[float])`**
  * **Purpose**: Calculates L2 magnitude of vector.
  * **Input**: list of floats.
  * **Output**: `float`
  * **Calling Function**: `embedding_demo.cosine_similarity`
  * **Called Functions**: None

* **`cosine_similarity(v1: list[float], v2: list[float])`**
  * **Purpose**: Evaluates angle alignment between two vectors.
  * **Input**: two lists of floats.
  * **Output**: `float`
  * **Calling Function**: `embedding_demo.run_demo`
  * **Called Functions**: `embedding_demo.dot_product`, `embedding_demo.magnitude`

* **`run_demo()`**
  * **Purpose**: Standard entry point explaining vector spacing and cosine similarity.
  * **Input**: None
  * **Output**: None
  * **Calling Function**: Main interpreter
  * **Called Functions**: `embedding_demo.cosine_similarity`

---

## 5. Dependency Diagram & Call Hierarchy

### Dependency Diagram
This diagram represents the import structure of our Python files:
```text
main.py
└── chat.py
    └── schemas.py
    └── chatbot.py
        ├── fastpath.py
        │   ├── greeting.py
        │   └── gibberish.py
        ├── intent.py
        ├── entity.py
        ├── context.py
        ├── knowledge_base.py
        │   └── search_engine.py
        └── response_generator.py
```

### Call Hierarchy (Execution flow for a standard query)
This hierarchy shows the order in which functions call other functions when processing a user request:
```text
main.chat_endpoint()
 └── chat.handle_chat_message()
      └── chatbot.get_bot_response()
           ├── search_engine.correct_spelling()
           ├── fastpath.process_fastpath()
           │    ├── greeting.is_greeting()
           │    └── gibberish.is_gibberish()
           ├── intent.detect_intent()
           ├── entity.extract_entities()
           ├── context.process_context()
           │    └── context.handle_context_query()
           ├── knowledge_base.query_knowledge_base()
           │    ├── knowledge_base.load_knowledge_files()
           │    └── search_engine.search_kb()
           │         ├── search_engine.clean_and_tokenize()
           │         ├── search_engine.build_search_candidates()
           │         └── search_engine.calculate_similarity_score()
           ├── response_generator.generate_response()
           └── context.add_to_history()
```

---

## 6. Learning Modules Mapping

The project's evolution is organized into distinct educational modules:

### Module 1: The FastPath Layer
* **Files**: `main.py`, `schemas.py`, `chat.py`, `chatbot.py`, `fastpath.py`, `greeting.py`, `gibberish.py`.
* **Core Code**: Rules validating greetings (`GREETING_PATTERN`) and gibberish patterns (keyboard crawls, letter flooding).
* **Flow**: FastPath immediately checks the query. If it's a greeting or gibberish, it returns early. Otherwise, it defaults to `"echo"`.

### Module 2: Intent Detection
* **Files**: `intent.py`.
* **Core Code**: The `INTENT_KEYWORDS` and `detect_intent` keyword parser.
* **Flow**: Scans clean user query for specific words (like `"pricing"`, `"support"`) and assigns an intent category.

### Module 3: Entity Extraction
* **Files**: `entity.py`.
* **Core Code**: The regex parsers in `extract_entities`.
* **Flow**: Inspects query to pull out variables (email, phone, amount, name, product) to populate the `entities` dictionary.

### Module 4: Conversation Context
* **Files**: `context.py`.
* **Core Code**: The global `sessions` dict, state updates in `process_context`, and query answers in `handle_context_query`.
* **Flow**: Checks if a message updates personal details (like *"My name is Kamlesh"*) or asks a question about state (like *"What is my name?"*). It updates and retrieves these variables from the session database.

### Module 5: Response Generation
* **Files**: `response_generator.py`.
* **Core Code**: The templates inside `generate_response`.
* **Flow**: Compiles final output text, dynamically incorporating extracted entities or formatting context queries.

### Module 6: Knowledge Base
* **Files**: `knowledge_base.py`, `knowledge/` JSON files.
* **Core Code**: Caches static data from `pricing.json`, `support.json`, `faq.json`, `company.json`, and `products.json`.
* **Flow**: Provides raw candidate questions and answers to the search engine to query matching facts.

### Module 7: Search and Ranking
* **Files**: `search_engine.py`.
* **Core Code**: Set calculations in `clean_and_tokenize`, fuzzy string comparison ratios in `calculate_similarity_score` and `search_kb`, and spelling correction in `correct_spelling`.
* **Flow**: Evaluates overlap percentages between user query tokens and cached KB questions, returning results that exceed the $30\%$ relevance gate.

### Module 8: Embeddings Sandbox
* **Files**: `embedding_demo.py`.
* **Core Code**: Cosine similarity calculation using dot products and vector length computations.
* **Flow**: A completely standalone math tutorial mapping words (like `"pricing"`, `"cost"`, and `"football"`) to manual 2D coordinates to demonstrate semantic vector search.

---

## 7. Architectural Code Review

As a Senior Software Architect and Reviewer, here is the technical assessment of our current implementation:

### 🟢 What is Good & Perfect for Learning
* **Pipes-and-Filters Design**: The step-by-step sequential routing makes it extremely easy to debug. You can trace exactly which file modified the message and why.
* **Separation of Concerns**: Keeping logic (`search_engine.py`, `intent.py`) completely separated from JSON data assets (`knowledge/*.json`) is an industry-standard best practice.
* **No External API Dependencies**: Running entirely locally on native libraries guarantees extreme speed, no API latency, and zero billing costs.

### 🟡 What Can Be Simplified
* **Keyword Intent Hardcoding**: The keywords inside `intent.py` are hardcoded. While simple, they could be loaded from a configuration YAML or JSON file like the Knowledge Base to make the system more dynamic.
* **Global `sessions` Memory**: The database state resides in a global Python dictionary `sessions = {}`. In a production environment, this would cause memory leaks over time. We would replace this with a fast key-value store database like Redis.

### 🔴 Unnecessarily Complex (But great for educational theory)
* **Gibberish Rules**: The consonant clusters and keyboard crawls inside `gibberish.py` are highly creative but complex to configure. In modern enterprise settings, this is typically handled by simple classifier microservices.

---

## 8. Manager Code Review FAQ

These are answers to questions a Software Engineering Manager is likely to ask during a project walkthrough:

* **Question 1: What is the main design pattern of this chatbot?**
  > **Answer**: It follows a **Pipes-and-Filters** architecture. The message acts as the data flowing through sequential "filters" (FastPath $\rightarrow$ Intent $\rightarrow$ Entity $\rightarrow$ Context $\rightarrow$ Knowledge Search $\rightarrow$ Response Generator). This keeps the code highly modular and allows us to easily turn stages on or off.

* **Question 2: How does the search engine rank answers without using an AI model?**
  > **Answer**: We tokenize the text and use character-level Levenshtein similarity ratios (from the `RapidFuzz` library) to evaluate the overlap score between the query tokens and our FAQ database keys. If the score is $\ge 30\%$, we retrieve that answer.

* **Question 3: Why do we have spelling correction at Step 0?**
  > **Answer**: By running a case-and-punctuation-preserving spell corrector first, we clean up the query (e.g. converting `"good morniing"` to `"good morning"`). This ensures that every downstream component (like simple greeting regexes or exact keyword intent matchers) functions correctly without needing to account for endless spelling permutations.

* **Question 4: What is the purpose of `embedding_demo.py`?**
  > **Answer**: It is a sandbox designed to teach vector mathematics. It demonstrates how words are converted to arrays of numbers (embeddings) and compared using cosine similarity to measure semantic alignment, laying the foundation for transitioning to real neural vector search.
