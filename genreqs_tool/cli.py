from genreqs_tool.genreqs import find_files_and_extract

# genreqs_tool/cli.py

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
"""
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract imports from a folder")
    parser.add_argument("folder", help="Target folder to scan")
    args = parser.parse_args()

    result = find_files_and_extract(args.folder)
    print("\n".join(result))
"""
