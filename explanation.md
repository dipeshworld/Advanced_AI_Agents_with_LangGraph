## How the Agent Works (LLM + LangGraph Overview)

### 1. Role of the LLM

The LLM (via OpenAI) is used to handle general-purpose queries such as explanations, definitions, or conversational responses. It acts as the default pathway when the input is not identified as a mathematical query.

The LLM is intentionally not used for mathematical computation. This ensures deterministic outputs, avoids hallucination, and reduces cost and latency.

---

### 2. Custom Math Functions

Four predefined functions are implemented for mathematical operations:

* plus(a, b)
* subtract(a, b)
* multiply(a, b)
* divide(a, b)

These functions form the only execution layer for math-related queries. Division includes error handling for division by zero.

---

### 3. Input Processing Pipeline

When a query is received, it goes through the following steps:

Step 1: Normalization
Natural language terms are converted into symbols. For example:

* "plus" becomes "+"
* "times" becomes "*"

Step 2: Expression Extraction
The system extracts valid mathematical expressions from the input string while ignoring irrelevant text.

Step 3: Safe Parsing
The extracted expression is parsed using Python’s Abstract Syntax Tree (AST), which ensures safe evaluation and prevents execution of arbitrary code.

Step 4: Evaluation
The parsed AST is recursively evaluated. Each operation node is mapped to the corresponding predefined math function.

---

### 4. LangGraph Agent Design

The agent is implemented using a state-based graph with two main nodes:

* Chatbot Node: Uses the LLM to generate responses for general queries
* Math Node: Executes mathematical expressions using the custom functions

A router function determines which node should handle the query.

---

### 5. Routing Logic

The router analyzes the input query:

* If a valid mathematical expression is detected, the query is routed to the Math Node
* Otherwise, it remains in the Chatbot Node and is handled by the LLM

---

### 6. Execution Flow

User Query
→ Chatbot Node receives input
→ Router evaluates the query
→ If math: Math Node executes and returns result
→ If not: LLM generates response

---

### 7. Multi-step Math Handling

The agent supports complex expressions such as:

* 4 + 5 * 2
* 10 + (6 / 2)

This is enabled by AST parsing, which naturally respects operator precedence (BODMAS/PEMDAS) and allows recursive evaluation of nested expressions.

---

### 8. Key Design Decisions

* Avoided use of eval() to eliminate security risks
* Used AST parsing for safe and structured computation
* Separated LLM reasoning from deterministic math execution
* Used LangGraph for clear control flow and scalability

---

### 9. Summary

The system combines:

* LLM-based reasoning for general queries
* Deterministic function-based execution for math
* Graph-based orchestration for routing and control

This results in an agent that is accurate, safe, and extensible.
