import argparse
from CodeAssist.CodeAssist import LLMRequest

def run_LLMRequest():
    parser = argparse.ArgumentParser(description="CLI LLM that roleplays as a terchpriest and helps you fix/improve your code")
    parser.add_argument("--string", help="Code sample")
    parser.add_argument("--filepath", help="Code file")
    parser.add_argument("--prompt", help="Prompt")
    args = parser.parse_args()
    LLMRequest(args.string, args.filepath, args.prompt)
