from pathlib import Path
import argparse
from typing import Dict
import pdf2bib
import pdf2doi


def paper2note(
    pdf: Path,
    pdf_rename_pattern: str = None,
    note_target_folder: Path = None,
    note_template_path: Path = None,
    note_filename_pattern: str = None,
    pdf2bib_config: Dict = None,
    pdf2doi_config: Dict = None,
):
    """Create a reference note from the extracted metadata of a paper and save it in a folder.
    Optionally also renames the pdf file according to the metadata.

    Args:
        pdf (Path): Path to the pdf file of the paper.
        pdf_rename_pattern (str, optional): Pattern to rename the pdf file. All entries
            of the metadata can be used as placeholders. Placeholder must be in curly braces.
            If not provided no renaming will be executed.
        note_target_folder (Path, optional): Folder where the note should be saved to.
            Can be an absolute path or relative to the directory from wich the script is
            called. Defaults to the directory of the pdf file.
        note_template_path (Path, optional): Path to the note template. Can be an absolute
            path or relative to the directory from wich the script is called. Defaults to
            a default note template.
        note_filename_pattern (str, optional): Pattern to name the note file. All entries
            of the metadata can be used as placeholders. Placeholder must be in curly braces.
            Defaults to the same name as the (renamed) pdf file.
        pdf2bib_config (Dict, optional): Configurations for pdf2bib. Defaults to None.
        pdf2doi_config (Dict, optional): Configurations for pdf2doi. Defaults to None.
    """
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
    # TODO check if renamed pdf already exists
    if pdf_rename_pattern is None:
        new_pdf_name = pdf.stem + ".pdf"
    else:
        new_pdf_name = pdf_rename_pattern.format(**bib)

    pdf.rename(pdf.parent / new_pdf_name)

    # create note.md
    if note_filename_pattern is None:
        note_filename = new_pdf_name
    else:
        note_filename = note_filename_pattern.format(**bib)

    note_content = note_template_path.read_text().format(**bib)

    # TODO check if note already exists
    if not note_target_folder.exists():
        note_target_folder.mkdir(parents=True)
    with open(note_target_folder / note_filename, "w") as f:
        f.write(note_content)


def parse_args() -> None:
    parser = argparse.ArgumentParser(
        description="Create a reference note from the extracted metadata of a paper and save it in a folder. Also renames the pdf file."
    )

    parser.add_argument("pdf", type=Path, help="Path to the pdf file of the paper.")
    parser.add_argument(
        "--pdf-rename-pattern",
        type=str,
        # default="{title}.pdf",
        help="Pattern to rename the pdf file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. If not provided no renaming will be executed.",
    )
    parser.add_argument(
        "--note-target-folder",
        type=Path,
        help="Folder where the note should be saved to. Can be an absolute path or relative to the directory from wich the script is called. Defaults to the directory of the pdf file.",
    )
    parser.add_argument(
        "--note-template-path",
        type=Path,
        help="Path to the note template. Can be an absolute path or relative to the directory from wich the script is called. Defaults to a default note template.",
    )
    parser.add_argument(
        "--note-filename-pattern",
        type=str,
        # default="{title}.md",
        help="Pattern to name the note file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to '{title}'.",
    )

    args = parser.parse_args()

    paper2note(
        args.pdf,
        args.pdf_rename_pattern,
        args.note_target_folder,
        args.note_template_path,
        args.note_filename_pattern,
    )


if __name__ == "__main__":
    # for quick testing
    pdf_path = Path(
        "C:/Users/mohes/Documents/LogSeqNotes/assets/storages/Papers/2304.02532.pdf"
    )
    assert pdf_path.exists()

    paper2note(pdf_path)
