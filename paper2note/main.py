from pathlib import Path
import argparse
from typing import Dict

from pdf2bib import pdf2bib


def create_logseq_page(template: str, bib: Dict):
    pass

def paper2logseq(pdf: Path, file_rename_pattern: str = "{{title}}", template_path: Path, note_target_folder, note_name_tempate):
    bib = pdf2bib(pdf)
    # create_logseq_page(logseq_template_path, bib)
    

def main():
    pass


if __name__ == "__main__":
    main()
