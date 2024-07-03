import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_config
from src.passage_selector import run_pipeline

def main(debug=False):
    config = load_config()
    query_text, results = run_pipeline(config, debug=debug)

    if debug:
        print(f"Query: {query_text}")
        for result in results:
            print(f"Document: {result[0]}\nPassage: {result[1]}\nScore: {result[2]}\n")

if __name__ == "__main__":
    debug_mode = True
    main(debug=debug_mode)
