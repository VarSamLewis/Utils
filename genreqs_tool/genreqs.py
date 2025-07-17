from pathlib import Path  
import ast
import json
import argparse
import logging
import sys


def _stdlib_modules():
    """Get a set of standard library module names."""
    return set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()


def check_module_against_stdlib(module_name):
    """Check if a module is part of the standard library."""
    stdlib_modules = _stdlib_modules()
    if module_name in stdlib_modules:
        logging.debug(f"Module {module_name} is part of the standard library.")
        return True
    else:
        logging.debug(f"Module {module_name} is not part of the standard library.")
        return False

def extract_from_py(filepath: Path):  
    with filepath.open('r', encoding='utf-8-sig') as f:  
        tree = ast.parse(f.read(), filename=str(filepath))
        logging.debug(f"AST parsed for {filepath}")

    modules = set()
    for node in ast.walk(tree):
        logging.debug(f"Visiting node: {ast.dump(node)}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split('.')[0])
                logging.debug(f"Found import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split('.')[0])
                logging.debug(f"Found import: {alias.name}")
    return modules

def extract_from_ipynb(filepath: Path):  
    with filepath.open('r', encoding='utf-8') as f:
        notebook = json.load(f)
        logging.debug(f"Notebook loaded for {filepath}")
    modules = set()
    for cell in notebook.get("cells", []):
        logging.debug(f"Processing cell: {cell.get('cell_type')}")
        if cell.get("cell_type") == "code":
            source_code = ''.join(cell.get("source", []))
            logging.debug(f"Source code extracted: {source_code[:50]}...")
            try:
                tree = ast.parse(source_code)
                logging.debug(f"AST parsed for cell in {filepath}")
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            modules.add(alias.name.split('.')[0])
                            logging.debug(f"Found import: {alias.name}")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            modules.add(node.module.split('.')[0])
                            logging.debug(f"Found import: {node.module}")
            except SyntaxError:
                logging.warning(
                    f"Syntax error in cell of {filepath}, skipping")
                continue  # Skip malformed cells
 
    return modules

def find_files_and_extract(folder):  
    folder = Path(folder)  
    all_modules = set()
    for path in folder.rglob("*"):
        logging.debug(f"Checking file: {path}")
        try:
            if path.suffix == ".py":
                all_modules |= extract_from_py(path)
            elif path.suffix == ".ipynb":
                all_modules |= extract_from_ipynb(path)
        except Exception as e:
            print(f"Error processing {path}: {e}")
    return sorted(all_modules)

def printreqs(folder):
    folder = Path(folder)  
    modules = find_files_and_extract(folder)
    modules = [mod for mod in modules if not check_module_against_stdlib(mod)]
    print("\n".join(modules))

def genreqs(folder):
    folder = Path(folder)  
    req_path = folder / "requirements.txt"  
    
    if req_path.exists():
        print("requirements.txt already exists, editing instead")
        req_path.unlink() 
        logging.debug(f"Deleted existing requirements.txt at {req_path}")

    modules = find_files_and_extract(folder)
    third_party_modules = [mod for mod in modules if not check_module_against_stdlib(mod)]
    try:
        with req_path.open('w', encoding='utf-8') as f:  
            for module in third_party_modules:
                f.write(module + "\n")
                logging.debug(f"Written libs to {req_path}")
        print(f"requirements.txt created at {req_path}")
    except Exception as e:
        print(f"Error writing requirements.txt: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract top-level imports from .py and .ipynb files")
    parser.add_argument("folder", help="Folder path to scan")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.ERROR,
        format='[%(levelname)s] %(message)s'
    )
    folder = Path(args.folder)  
    modules = find_files_and_extract(folder)
    print("\n".join(modules))

if __name__ == "__main__":
    main()
