============================================================
TWENTY QUESTIONS FOR ARTIFICIAL LABS
============================================================

This is my submission for the "Twenty Questions" game using an LLM, as part of my application as an AI intern.
It includes:

    Task 1: Human vs LLM
    Task 2: LLM vs LLM
    Final Combined App with 3 playable modes

The LLM used is the one provided via the provided OpenAI-compatible API proxy.

============================================================
 1. SETUP INSTRUCTIONS
============================================================

This project is designed to run inside a virtual environment.

Create and activate the virtual environment:

Linux / macOS:
    python3 -m venv venv
    source venv/bin/activate

Windows (PowerShell):
    python -m venv venv
    venv\Scripts\activate

Install required dependencies:

    pip install -r requirements.txt

Add your API key:

You MUST set the environment variable:

    CANDIDATE_API_KEY

Create a file named .env in the project root:

    CANDIDATE_API_KEY=your_api_key_here

============================================================
 4. RUNNING THE GAMES
============================================================


Run the Final Combined App (recommended):

    python app/app_cli.py

You will see this menu:

    1. Human vs LLM
    2. LLM vs Human
    3. LLM vs LLM
    4. Quit

Task 1 Only (Human vs LLM):

    python task1/task1_human_vs_llm.py

 4.3 Run Task 2 Only (LLM vs LLM):

    python task2/task2_llm_vs_llm.py