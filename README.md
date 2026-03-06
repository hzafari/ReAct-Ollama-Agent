# Custom ReAct Agent from Scratch (Local LLM)


A lightweight **ReAct-based AI agent** that can reason step-by-step, use external tools, and retrieve information from local documents. This is a high-performance reasoning agent built without heavy frameworks and demonstrates the core mechanics of **ReAct (Reason + Act) loops**, autonomous tool-chaining, and context window optimization using local LLMs via Ollama.

The agent runs with a **local LLM (Ollama)** and demonstrates how modern AI systems combine **reasoning + tool usage + document search** to answer questions.

This project implements a **ReAct (Reason + Act) agent architecture** where the language model:

1. Thinks about the problem
2. Chooses an action (tool)
3. Executes the tool
4. Observes the result
5. Repeats until the final answer is produced

The system includes tools for:

* Searching documents
* Reading files
* Performing calculations

The agent maintains a **scratchpad reasoning trace**, allowing you to inspect how the answer was produced.

---

## Key Features

* **Autonomous Tool-Chaining:** The agent independently decides to search for a file, extract its name, and read its content without human intervention.
* **State Management:** Implements a custom "Scratchpad" and "Knowledge Base" to maintain reasoning history and permanent facts.
* **Context Window Optimization:** Uses a sliding-window "Prompt Pruning" technique to prevent local LLM latency and token overflow.
* **Observability:** Automatically generates **Markdown Reasoning Traces** for every interaction, showing the "inner monologue" of the AI.


# Features

* ReAct reasoning loop
* Local LLM integration (via Ollama)
* Tool-based architecture
* Document retrieval workflow
* Keyword expansion for better search
* Safe file access inside a controlled directory
* Step-by-step reasoning trace export
* Knowledge base accumulation from observations
* JSON-only agent outputs for reliability

---

## Tool Suite

| Tool | Purpose | Technical Implementation |
| :--- | :--- | :--- |
| **file_search** | Keyword Discovery | Scans directory for relevant metadata/filenames. |
| **file_reader** | Data Extraction | Safely reads and sanitizes text from local storage. |
| **calculator** | Logic/Math | Offloads arithmetic to Python to prevent LLM hallucinations. |

---

## The Engineering Challenges (And my Solutions)

### 1. The "Obsessive Loop" Problem
**The Issue:** Local LLMs often get stuck repeating the same search if they don't see a clear path to the next step.
**The Solution:** I implemented **Success-Nudge Strings** in the tool outputs. By adding instructions like *"You have the filename; now use file_reader,"* I successfully guided the model from discovery to extraction.

### 2. Context Window Drifting
**The Issue:** Long reasoning chains caused "Attention Drift," where the LLM forgot its original goal.
**The Solution:** I engineered a **Knowledge Base vs. Scratchpad** architecture. Permanent facts are stored separately, while the active reasoning "Scratchpad" is pruned to the last 500 characters, keeping the model focused and fast.

### 3. Tool Disambiguation
**The Issue:** The agent confused `file_search` with `file_reader`.
**The Solution:** I used **Semantic Routing** via specific Python docstrings. By defining strict "Positive Triggers" and "Negative Constraints" in the tool descriptions, I reached 100% accuracy in tool selection.

---

## Sample Trace: Multi-Step Reasoning

**Question:** *"Who is invited to the party?"*

1.  **Thought:** I need to find information about invitations. I'll start with `file_search`.
2.  **Action:** `file_search("invited")`
3.  **Observation:** Found `invitation.txt`.
4.  **Thought:** I have the filename. Now I will read its content.
5.  **Action:** `file_reader("invitation.txt")`
6.  **Observation:** *"Ali and Reza are invited..."*
7.  **Final Answer:** Ali, Reza, and Mohammad are the guests invited to the party.

---

## Technical Stack

* **Language:** Python 3.10+
* **LLM Runner:** Ollama (Llama 3 / Mistral)
* **Design Pattern:** ReAct (Reasoning and Acting)
* **Data Handling:** JSON Parsing with Regex-based safety fallbacks

---

## How to Run

1.  **Clone the repo:** `git clone <your-repo-url>`
2.  **Ensure Ollama is running:** `ollama serve`
3.  **Setup Documents:** Place your text files in the `docs/` folder.
4.  **Run the Agent:** `python main.py`

---
*Created as part of an AI Engineering portfolio to demonstrate low-level LLM orchestration.*