import argparse
from genreqs_tool.genreqs import printreqs, genreqs

def run_printreqs():
    parser = argparse.ArgumentParser(description="Print imports from Python and Jupyter files")
    parser.add_argument("folder", help="Target folder to scan")
    args = parser.parse_args()
    printreqs(args.folder)

def run_genreqs():
    parser = argparse.ArgumentParser(description="Generate requirements.txt from top-level imports")
    parser.add_argument("folder", help="Target folder to scan")
    args = parser.parse_args()
    genreqs(args.folder)

