# genreqs-tool

**genreqs** is a lightweight CLI utility for scanning Python files (`.py`) and Jupyter notebooks (`.ipynb`) in a given folder and extracting the top-level imported modules. Designed for quick dependency auditing and scaffolding your `requirements.txt` with minimal fuss.

## What It Does

- Recursively scans all `.py` and `.ipynb` files in a folder  
- Parses `import` and `from ... import ...` statements using AST  
- Returns a deduplicated, alphabetized list of top-level module names  

## Installation

Make sure Poetry is installed. Then run:

poetry install


---

### Usage

From the terminal:

Print:
poetry run printreqs <path_to_folder>

Write:
poetry run genreqs <path_to_folder>

Add a --Debug flag to see debug info


To skip `poetry run`, you can activate the Poetry shell:

poetry shell
genreqs <path_to_folder>

Or add Poetry’s virtualenv `Scripts` folder to your system PATH for global access.

## Output

Print:
Displays a list of detected imports to stdout:

matplotlib  
numpy  
pandas  
scikit-learn

Write:

Writes the imports to `requirements.txt` in the specified folder:

You can pipe it to a file manually:

poetry run genreqs . > raw_reqs.txt

Coming soon: `--out` flag, exclusion filters, and integration with your requirements writer.

How to run tests:
poetry run python -m genreqs_tool.test_cases

# Kairos
Kairos is a daemon-themed CLI assistant that answers your questions with cryptic wisdom and theatrical flair. Inspired by the 40k universe, Kairos Fateweaver delivers two answers to every question — one true, one false — and leaves you to divine your fate.

## What it does
Accepts a natural language question via CLI

Sends the question to the OpenAI API with a custom prompt

Returns two helpful answers: one correct, one misleading

Speaks in the voice of Kairos, the Great Oracle of Tzeentch

```bash
poetry run provide_guidance "What will the weather be tomorrow in Bristol?"
```

Kairos will respond with two answers, cloaked in mystery and dripping with daemon wisdom.
Kairos speaks in the third person and uses colourful, cryptic language.
Both answers are helpful, but only one is true — and Kairos will never tell.

Requirements:

Libaries:
- `openai` for API interaction
- `rich` for pretty terminal output
- `petry` for CLI handling
- An OpenAI API key set in your environment variables, please see OpenAI documentation for details.
