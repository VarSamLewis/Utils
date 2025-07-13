import os
import ast
import json
import argparse

def extract_from_py(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        tree = ast.parse(f.read(), filename=filepath)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split('.')[0])
    return modules

def extract_from_ipynb(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    modules = set()
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source_code = ''.join(cell.get("source", []))
            try:
                tree = ast.parse(source_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            modules.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            modules.add(node.module.split('.')[0])
            except SyntaxError:
                continue  # Skip malformed cells
    return modules


def find_files_and_extract(folder):
    all_modules = set()
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.endswith(".py"):
                    all_modules |= extract_from_py(path)
                elif file.endswith(".ipynb"):
                    all_modules |= extract_from_ipynb(path)
            except Exception as e:
                print(f"Error processing {path}: {e}")
    return sorted(all_modules)

""" Untested code I wrote directly on Github do not trust until verified"""
def printreqs(folder):

    modules = find_files_and_extract(folder)
    print("\n".join(modules))

def genreqs(folder):
    req_path = os.path.join(folder, "requirements.txt")
    
    if os.path.exists(req_path):
        print("requirements.txt already exists")
        return

    reqs = find_files_and_extract(folder)
    try:
        with open(req_path, 'w', encoding='utf-8') as f:
            for req in reqs:
                f.write(req + "\n")
        print(f"requirements.txt created at {req_path}")
    except Exception as e:
        print(f"Error writing requirements.txt: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract top-level imports from .py and .ipynb files")
    parser.add_argument("folder", help="Folder path to scan")
    args = parser.parse_args()
    modules = find_files_and_extract(args.folder)
    print("\n".join(modules))

if __name__ == "__main__":
    main()
