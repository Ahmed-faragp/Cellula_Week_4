#  Self-Learning Coding Agent (RAG + Memory + OpenRouter)

This project is an **AI coding agent** that combines:

-  Retrieval-Augmented Generation (RAG)
-  Persistent conversation memory
-  Intent classification (coding vs explanation)
-  Self-learning from user input

Unlike basic RAG systems, this agent can **learn new code and explanations dynamically** when it fails to retrieve relevant context.

---

##  Features

###  1. Semantic Code Retrieval
- Uses **ChromaDB** with embeddings (`all-MiniLM-L6-v2`)
- Preloaded with **HumanEval dataset**
- Retrieves top-k relevant coding examples

---

###  2. Self-Learning System
If no relevant context is found:
- The agent asks the user to teach it:
  - Function name
  - Code (multi-line supported)
  - Explanation
- Stores new knowledge in vector DB

---

###  3. Persistent Memory
- Uses `ConversationSummaryMemory`
- Stores chat history in `memory.json`
- Maintains long-term context across runs

---

###  4. Intent Classification
Automatically detects:
- `"coding"` → generate code
- `"explanation"` → explain concepts/code

---

###  5. Smart Prompting System

3 modes:
- **Coding mode**
- **Explanation mode**
- **Learning mode**

Rules:
- Uses retrieved context if available
- If no context → enters learning mode
- Avoids hallucinating APIs

---

##  Architecture

```
User Input
   ↓
Retrieve Context (ChromaDB)
   ↓
Confident?
   ├──  No → Ask user to teach → Store in DB
   └──  Yes
         ↓
   Classify Intent (LLM)
         ↓
   Build Prompt (Context + Memory)
         ↓
   LLM (OpenRouter - LLaMA 3)
         ↓
   Save Memory
         ↓
   Output + Debug Info
```

---

##  Project Structure

```
.
├── rag.py              # Main agent loop
├── chroma_vdb.py       # Vector DB + retrieval
├── memory.py           # Memory system (persistent)
├── prompt_sys.py       # Prompt templates (3 modes)
├── routing.py          # Intent classification
├── memory.json         # Stored conversation history
├── chroma_db/          # Vector database (auto-created)
├── requirements.txt
└── README.md
```

---

##  Installation

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo

pip install -r requirements.txt
```

---

##  Environment Setup

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

##  Run the Agent

```bash
python rag.py
```

---

##  Example Usage

```
Ask a question: How do I reverse a linked list?
```

### Case 1: Context Found
- Retrieves relevant example
- Generates answer using context + memory

### Case 2: No Context Found
```
I don't know this function yet, please teach me:
1. function name
2. code
3. explanation
```

Then:
```
function name:
my_function

Enter code:
<your code>

explanation:
<your explanation>
```

 The system **learns and stores it permanently**

---

##  Memory System

- Stores conversations in `memory.json`
- Summarizes them automatically
- Injected into every prompt:

```python
memory_summary = conversation.memory.buffer
```

---

##  Retrieval Logic

```python
results = vectorstore.similarity_search_with_score(query, k=3)

if best_score > 1.0:
    return None, False
```

- Uses **distance score threshold**
- Rejects low-confidence matches

---


