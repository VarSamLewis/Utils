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

```markdown
## Usage

From the terminal:

poetry run genreqs <path_to_folder>

Examples:

poetry run genreqs .
poetry run genreqs C:\Users\samle\source\repos\my_project

To skip `poetry run`, you can activate the Poetry shell:

poetry shell
genreqs <path_to_folder>

Or add Poetry’s virtualenv `Scripts` folder to your system PATH for global access.

## Output

Displays a list of detected imports to stdout:

matplotlib  
numpy  
pandas  
scikit-learn

You can pipe it to a file manually:

poetry run genreqs . > raw_reqs.txt

Coming soon: `--out` flag, exclusion filters, and integration with your requirements writer.
