from genreqs_tool.genreqs import find_files_and_extract

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract imports from a folder")
    parser.add_argument("folder", help="Target folder to scan")
    args = parser.parse_args()

    result = find_files_and_extract(args.folder)
    print("\n".join(result))