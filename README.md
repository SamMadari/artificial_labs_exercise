# Twenty Questions Artificial Labs Submission

This repository contains my implementation of a **Twenty Questions** game powered by an **LLM**, built as part of the Artificial Labs internship application.

It includes:

* **Task 1:** Human vs LLM
* **Task 2:** LLM vs LLM
* **Final Combined App:** Three fully playable modes

The project uses the **OpenAI-compatible API proxy** provided for the challenge.

---

## 🚀 1. Setup Instructions

This project is designed to run in a Python virtual environment.

### 1.1 Create & Activate Virtual Environment

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```bash
python -m venv venv
venv\Scripts\activate
```

### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 1.3 Add Your API Key

The app requires an environment variable:

```
CANDIDATE_API_KEY
```

Create a `.env` file in the repository root:

```
CANDIDATE_API_KEY=your_api_key_here
```

---

## 🎮 2. Running the Games

### 2.1 Run the Full Combined App (Recommended)

```bash
python app/app_cli.py
```

You’ll see this menu:

```
1. Human vs LLM
2. LLM vs Human
3. LLM vs LLM
4. Quit
```

### 2.2 Run Task 1 Only — Human vs LLM

```bash
python task1/task1_human_vs_llm.py
```

### 2.3 Run Task 2 Only — LLM vs LLM

```bash
python task2/task2_llm_vs_llm.py
```
