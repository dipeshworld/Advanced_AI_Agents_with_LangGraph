# 🧠 LangGraph Math + General Query Agent

This project implements a **LangGraph-based intelligent agent** that can:

* 💬 Answer general questions using an LLM (OpenAI)
* 🧮 Solve mathematical queries using predefined functions
* 🔀 Seamlessly route between LLM and math tools
* ⚡ Support both simple and multi-step math expressions

---

## 🚀 Features

* ✅ LangGraph state-based agent architecture
* ✅ OpenAI-powered reasoning for general queries
* ✅ Custom math tool integration:

  * `plus(a, b)`
  * `subtract(a, b)`
  * `multiply(a, b)`
  * `divide(a, b)` (with zero-division handling)
* ✅ Supports:

  * Symbolic math → `4+14`, `10/2`
  * Natural language → `4 plus 14`, `divide 10 by 2`
  * Multi-step expressions → `4 + 5 * 2`, `10 + (6/2)`
* ✅ Safe execution using Python AST (no `eval`)

---

## 🏗️ Architecture

```
User Query
   ↓
Chatbot Node (LLM)
   ↓
Router (Decision Engine)
   ↓
 ┌───────────────┬───────────────┐
 │               │               │
Math Node     LLM Response     END
 │
 END
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

### 2. Create Virtual Environment (Python 3.10 recommended)

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup Environment Variables

Set your OpenAI API key:

```bash
# Mac/Linux
export OPENAI_API_KEY="your_api_key_here"

# Windows (PowerShell)
setx OPENAI_API_KEY "your_api_key_here"
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🧪 Example Queries

### 💬 General Queries

* `What is data engineering?`
* `Explain generative AI`

### 🧮 Basic Math

* `4+14`
* `10 divided by 2`
* `6 * 7`

### 🔢 Multi-step Math

* `4 + 5 * 2`
* `10 + (6/2)`
* `100 / (5 + 5)`

### 🗣️ Natural Language Math

* `What is 4 plus 5 times 2?`

---

## 🧠 How It Works

### 1. Input Normalization

Natural language math terms are converted to symbols:

* `plus → +`
* `times → *`

### 2. Expression Extraction

Only valid math expressions are extracted from the input.

### 3. Safe Evaluation

* Uses Python `ast` to parse expressions
* Maps operations to predefined functions
* Prevents unsafe execution (no `eval`)

### 4. Routing Logic

* Math query → handled by Math Node
* General query → handled by LLM

---

## ⚠️ Error Handling

* Division by zero is safely handled
* Invalid expressions return a graceful message

---

## 🛠️ Tech Stack

* Python 3.10
* LangGraph
* LangChain
* OpenAI API
* AST (safe math evaluation)

---

## 🔮 Future Enhancements

* 🔹 LLM-based tool selection (function calling)
* 🔹 Support for advanced math (power, modulus)
* 🔹 Memory-enabled conversations
* 🔹 FastAPI deployment
* 🔹 Docker containerization

---

## 👨‍💻 Author

Built as part of a **GenAI + Data Engineering learning project**.

---

## 📜 License

This project is for educational purposes. Modify and use as needed.
