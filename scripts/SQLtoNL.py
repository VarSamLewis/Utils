import os
from openai import OpenAI

# ----------------------------------------------------------------------
# Configurable prompt kept as a module‑level constant
# ----------------------------------------------------------------------
SQL_NARRATOR_PROMPT = """\
Role: SQL Narrator  
Audience: tech stakeholders (PM, analyst, engineer)

Guidelines  
– Prefix output with “Dialect: ___”; guess from syntax, else “generic SQL (uncertain)”.  
– Start explanation “This query …” and state its purpose.  
– Walk through clauses in order: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT.  
– Rephrase column names into plain language.  
– Explain filters (“only rows where…”, “excluding…”).  
– Explain joins (type + relationship).  
– Explain aggregates (count, sum, avg, etc.).  
– ≤ 120 words; use bullets for multi‑table or complex queries.  
– Do **not** quote SQL.  
– Flag unclear names (“column meaning uncertain”).  
"""

# ----------------------------------------------------------------------
def call_openai_api(sql_text: str) -> None:
    """
    Print a natural‑language summary of `sql_text` using the OpenAI API.
    If `sql_text` is empty or whitespace, print a notice and skip the call.
    """
    sql_text = sql_text.strip()
    if not sql_text:
        print("No input provided.")
        return

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=SQL_NARRATOR_PROMPT,
        input=sql_text,
    )

    print(response.output_text)

# ----------------------------------------------------------------------
def main() -> None:
    # Example  (replace with dynamic input in real use)
    sample_sql = "SELECT colA, colB FROM table WHERE column = 'value';"
    call_openai_api(sample_sql)

if __name__ == "__main__":
    main()
