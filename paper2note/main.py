from pathlib import Path
import argparse
from typing import Dict
from datetime import datetime
import time
import pdf2bib
import pdf2doi


def paper2note(
    pdf: Path,
    pdf_rename_pattern: str = "{title}.pdf",
    note_target_folder: Path = None,
    note_template_path: Path = None,
    note_filename_pattern: str = "{title}.md",
    pdf2bib_config: Dict = None,
    pdf2doi_config: Dict = None,
):
    # handle default values, allow also str instead of Path, and make paths absolute
    note_target_folder = note_target_folder or pdf.parent
    note_target_folder = Path(note_target_folder)
    if not note_target_folder.is_absolute():
        note_target_folder = Path.cwd() / note_target_folder

    note_template_path = (
        note_template_path
        or Path(__file__).parent.parent / "templates" / "default_note_template.md"
    )
    note_template_path = Path(note_template_path)
    if not note_template_path.is_absolute():
        note_template_path = Path.cwd() / note_template_path

    pdf2bib_config = pdf2bib_config or {}
    pdf2doi_config = pdf2doi_config or {}

    # set config values for underlying libraries
    for config_name, config_value in pdf2doi_config.items():
        pdf2doi.config.set(config_name, config_value)
    for config_name, config_value in pdf2bib_config.items():
        pdf2bib.config.set(config_name, config_value)

    # extract metadata
    bib = pdf2bib.pdf2bib(str(pdf))["metadata"]

    # rename pdf
    pdf.rename(pdf.parent / pdf_rename_pattern.format(**bib))

    # create note.md
    note = note_template_path.read_text().format(**bib)
    note_filename = note_filename_pattern.format(**bib)

    # create the file
    if not note_target_folder.exists():
        note_target_folder.mkdir(parents=True)
    with open(note_target_folder / note_filename, "w") as f:
        f.write(note)


def main():
    parser = argparse.ArgumentParser(
        description="Create a reference note from the extracted metadata of a paper and save it in a folder. Also renames the pdf file."
    )

    parser.add_argument("pdf", type=Path, help="Path to the pdf file of the paper.")
    parser.add_argument(
        "--pdf-rename-pattern",
        type=str,
        default="{title}.pdf",
        help="Pattern to rename the pdf file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to '{title}'.",
    )
    parser.add_argument(
        "--note-target-folder",
        type=Path,
        help="Folder where the note should be saved to. Can be an absolute path or relative to the directory from wich the script is called. Defaults to the directory of the pdf file.",
    )
    parser.add_argument(
        "--note-template-path",
        type=Path,
        help="Path to the note template. Can be an absolute path or relative to the directory from wich the script is called. Defaults to the default note template.",
    )
    parser.add_argument(
        "--note-filename-pattern",
        type=str,
        default="{title}.md",
        help="Pattern to name the note file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to '{title}'.",
    )

    args = parser.parse_args()

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"C:/Users/mohes/Desktop/{current_time}.txt", "w") as f:
        f.write("")

    print("sdfsdfsdfsdfsdf")
    time.sleep(10)

    # paper2note(
    #     args.pdf,
    #     args.pdf_rename_pattern,
    #     args.note_target_folder,
    #     args.note_template_path,
    #     args.note_filename_pattern,
    # )


if __name__ == "__main__":
    pdf_path = Path(
        "C:/Users/mohes/Documents/LogSeqNotes/assets/storages/Papers/2304.02532.pdf"
    )
    assert pdf_path.exists()

    paper2note(pdf_path)
