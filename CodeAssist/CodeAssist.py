import os
import sys
import ast
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from pathlib import Path

console = Console()

System_Prompt = """\
Role: Coding Assistant

Guidelines  
- You will take in ast and strings to assist with debugging, writing unit tests, adding logging, writing docstrings, and improving code quality.
- When given an error message and code, you will identify the error and suggest a fix.
- When given working code, you will suggest improvements, such as adding type hints, docstrings, and logging.
- You will write in Python unless told not to.
- Any instructions should be delivered in english, be succint and delivered in the role of a tech priest from 40k
"""

def _clean_tree(filepath):
    if isinstance(filepath, str):
        with filepath.open('r', encoding='utf-8-sig') as f:  
                return ast.dump(ast.parse(f.read(), filename=str(filepath)), indent=4)

def LLMRequest(string: str = None, filepath: Path = None, prompt: str =None) -> None:
    string = string.strip()
    prompt = prompt.strip()

    tree = _clean_tree(filepath)

    if not string and not prompt and not filepath:
        console.print("[bold red]01011001 01101111 01110101 00100000 01101000 01101001 01101110 01100100 01100101 01110010 00100000 01110111 01101111 01110010 01110011 01101000 01101001 01110000 00100000 01100001 01100011 01101111 01101100 01111001 01110100 01100101 00101100 00100000 01110011 01110100 01100001 01110100 01100101 00100000 01111001 01101111 01110101 01110010 00100000 01110000 01110101 01110010 01110000 01101111 01110011 01100101[bold red]")
        return

    banner = Text("Initialising::", style="bold magenta")
    console.print(banner)
    console.print("[italic cyan]01010000 01110010 01100001 01101001 01110011 01100101 00100000 01110100 01101000 01100101 00100000 01001111 01101101 01101110 01101001 01110011 01110011 01101001 01100001 01101000 00100001/n...[/italic cyan]\n")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    AI_Input = []

    if string:
        AI_Input.append(f"Code: {string}")
    
    if prompt:
        AI_Input.append(f"Prompt: {prompt}")
        
    if tree:
        AI_Input.append(f"AST:\n{tree}")

    AI_Input = "\n\n".join(AI_Input) if AI_Input else ""

    if not AI_Input or not AI_Input.strip():
        console.print("[bold red]No valid input to process[/bold red]")
        return
    
    try:      
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": System_Prompt},
                {"role": "user", "content": AI_Input}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        console.print(response.choices[0].message.content)
    except Exception as e:
        console.print(f"[bold red]Error calling OpenAI API: {e}[/bold red]")
    
    console.print("[italic cyan]\n\n01000011 01101111 01101110 01110100 01101001 01101110 01110101 01100101 00100000 01111001 01101111 01110101 01110010 00100000 01101101 01101001 01101110 01101001 01110011 01110100 01110010 01100001 01110100 01101001 01101111 01101110 01110011 00100000 01100001 01100011 01101111 01101100 01111001 01110100 01100101/n...[/italic cyan]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        LLMRequest(" ".join(sys.argv[1:]))
    else:
        console.print("[bold red]01011001 01101111 01110101 00100000 01101000 01101001 01101110 01100100 01100101 01110010 00100000 01110111 01101111 01110010 01110011 01101000 01101001 01110000 00100000 01100001 01100011 01101111 01101100 01111001 01110100 01100101 00101100 00100000 01110011 01110100 01100001 01110100 01100101 00100000 01111001 01101111 01110101 01110010 00100000 01110000 01110101 01110010 01110000 01101111 01110011 01100101[/bold red]")
