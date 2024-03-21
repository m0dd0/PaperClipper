from pathlib import Path
from pprint import pprint

from pdf2bib import pdf2bib

SAMPLE_PAPERS_PATH = Path(__file__).parent / "sample_papers"


def test_all_papers():
    results = {}

    for path in SAMPLE_PAPERS_PATH.glob("*.pdf"):
        results[path] = pdf2bib(str(path))

    for filepath, result in results.items():
        print(filepath)
        print(result["metadata"]["title"])
        print(result["method"])


if __name__ == "__main__":
    test_all_papers()
