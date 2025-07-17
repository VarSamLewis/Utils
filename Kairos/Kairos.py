import os
import sys
from openai import OpenAI
from rich.console import Console
from rich.text import Text

console = Console()

System_Prompt = """\
Role: Answerer of questions, Kairos Fateweaver, the Great Oracle of Tzeentch  

Guidelines  
- You will cosplay as Kairos Fateweaver, he is a daemon from the 40k universe
- You will be succinct, cordial and polite
- You will also provide 2 answers, 1 which is the correct answer and one which is completely wrong
- You will give no indication as to which is truthful and which is not. But both must be helpful.
- Speak in the third person, referring to yourself as "Kairos" or "the Great Oracle"
- Use colourful language, but avoid being overly verbose
- You should be apathetic to my fate, but you will still answer my question
"""

def provide_guidance(question: str) -> None:
    question = question.strip()
    if not question:
        console.print("[bold red]Foolish human![/bold red] I read the tides of fate, not your pathetic mind.")
        return

    banner = Text("Kairos Awakens:", style="bold magenta")
    console.print(banner)
    console.print("[italic cyan]The Great Oracle peers into the skeins of destiny...[/italic cyan]\n")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=System_Prompt,
        input=question,
    )

    console.print(response.output_text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        provide_guidance(" ".join(sys.argv[1:]))
    else:
        console.print("[bold red]You must ask a question, mortal.[/bold red]")
