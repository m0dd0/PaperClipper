from pathlib import Path
import argparse
from typing import Dict
import logging
import string
import json
import pprint

import pdf2bib
import pdf2doi
from pathvalidate import sanitize_filepath

logger = logging.getLogger("paper2note")


def input_validate_path(path: str, must_exist: bool = False) -> Path:
    # TODO docstring
    path = Path(path)
    if not path.is_absolute():
        path = Path.cwd() / path

    if must_exist and not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    return path


def clean_metadata(extraction_result: Dict) -> Dict:
    """Clean the metadata extracted from a PDF file and add some aggrgated fields.

    Args:
        extraction_result (Dict): The metadata extracted from a PDF file as returned by pdf2bib.

    Returns:
        Dict: The cleaned metadata which is used for the templating operation.
    """
    metadata = extraction_result["metadata"] or {}
    validation_info = extraction_result["validation_info"] or {}
    if isinstance(validation_info, str):
        validation_info = json.loads(validation_info)
    validation_info = dict(validation_info)

    authors_list = metadata.get("author", [])
    authors_list = [f"{author['given']} {author['family']}" for author in authors_list]

    cleaned_metadata = {
        "title": metadata.get("title", "<no title found>"),
        "authors": ", ".join(authors_list) if authors_list else "<no authors found>",
        "year": metadata.get("year") or "????",
        "month": metadata.get("month") or "??",
        "day": metadata.get("day") or "??",
        "journal": metadata.get("journal")
        or metadata.get("ejournal")
        or "<no journal found>",
        "doi": metadata.get("doi") or "<no doi found>",
        "url": metadata.get("url") or "<no url found>",
        "volume": metadata.get("volume") or "<no volume found>",
        "page": metadata.get("page") or "<no page found>",
        "type": metadata.get("ENTRYTYPE") or "article",
        "abstract": (
            validation_info.get("summary")
            or validation_info.get("abstract")
            or "<no abstract found>"
        ).replace("\n", " "),
        "bibtex": extraction_result.get("bibtex") or "<no bibtex found>",
        "extraction_method": extraction_result["method"],
        "logseq_author_listing": "[[" + "]], [[".join(authors_list) + "]]",
    }

    for i, author in enumerate(authors_list):
        cleaned_metadata[f"author_{i+1}"] = author

    if authors_list:
        cleaned_metadata["author_last"] = authors_list[-1]

    return cleaned_metadata


def format_pattern(string_to_format: str, data: Dict, is_filename: bool = False) -> str:
    # TODO docstring
    field_names = [
        field
        for _, field, _, _ in string.Formatter().parse(string_to_format)
        if field is not None
    ]
    for field_name in field_names:
        if field_name not in data:
            string_to_format = string_to_format.replace(
                f"{{{field_name}}}", f"<'{field_name}' IS AN INVALID PLACEHOLDER>"
            )
            logger.warning(f"'{field_name}' IS AN INVALID PLACEHOLDER")
    string_to_format = string_to_format.format(**data)

    if is_filename:
        string_to_format = sanitize_filepath(string_to_format)

    return string_to_format


def get_relative_logseq_path(path: Path) -> Path:
    # TODO docstring
    path = path.resolve()
    full_path = path

    while not (path / "logseq").exists():
        path = path.parent
        if path == Path.home():
            return None

    return full_path.relative_to(path)


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
            Defaults to the same as the pdf_rename_pattern.
        pdf2bib_config (Dict, optional): Configurations for pdf2bib. Defaults to None.
        pdf2doi_config (Dict, optional): Configurations for pdf2doi. Defaults to None.
    """
    ### handle default values, allow also str instead of Path, and make paths absolute ###
    pdf = input_validate_path(pdf, must_exist=True)
    if not pdf.suffix == ".pdf":
        raise ValueError("The provided file is not a pdf file.")

    pdf_rename_pattern = pdf_rename_pattern or pdf.stem

    note_target_folder = note_target_folder or pdf.parent
    note_target_folder = input_validate_path(note_target_folder)

    note_template_path = (
        note_template_path
        or Path(__file__).parent.parent / "templates" / "default_note_template.md"
    )
    note_template_path = input_validate_path(note_template_path, must_exist=True)

    note_filename_pattern = note_filename_pattern or pdf_rename_pattern

    pdf2bib_config = pdf2bib_config or {}
    pdf2doi_config = pdf2doi_config or {"save_identifier_metadata": False}

    ### set config values for underlying libraries ###
    for config_name, config_value in pdf2doi_config.items():
        pdf2doi.config.set(config_name, config_value)
    for config_name, config_value in pdf2bib_config.items():
        pdf2bib.config.set(config_name, config_value)

    ### extract metadata ###
    logger.info(f"Extracting metadata from {pdf}.")
    result = pdf2bib.pdf2bib(str(pdf))
    if not result["metadata"]:
        logger.warning(f"No metadata found for {pdf}.")
        # TODO popup
        return
    data = clean_metadata(result)

    # somttimes a google cookie is set when using websearch to extract the doi
    # we remove it to keep the folder clean
    if (pdf.parent / ".google-cookie").exists():
        (pdf.parent / ".google-cookie").unlink()
        logger.info("Removed google cookie.")

    ### rename pdf ###
    new_pdf_path = pdf.parent / f"{format_pattern(pdf_rename_pattern, data, True)}.pdf"
    if new_pdf_path != pdf and not new_pdf_path.exists():
        logger.info(f"Renaming {pdf} to {new_pdf_path}.")
        pdf.rename(new_pdf_path)
    else:
        logger.info(f"Did not rename {pdf}.")
    data["path"] = str(new_pdf_path)
    data["relative_logseq_path"] = str(get_relative_logseq_path(new_pdf_path))
    # logger.info(f"Metadata extracted: {pprint.pformat(data)}")

    ### create note.md ###
    note_path = (
        note_target_folder / f"{format_pattern(note_filename_pattern, data, True)}.md"
    )
    note_content = format_pattern(note_template_path.read_text(), data)

    if not note_path.exists():
        if not note_target_folder.exists():
            note_target_folder.mkdir(parents=True)

        logger.info(f"Creating note at {note_path}.")
        with open(note_path, "w") as f:
            f.write(note_content)
    else:
        logger.warning(f"Did not create note at {note_path} because it already exists.")
        # TODO popup


def parse_args() -> None:
    parser = argparse.ArgumentParser(
        description="Create a reference note from the extracted metadata of a paper and save it in a folder. Also renames the pdf file."
    )

    parser.add_argument("pdf", type=Path, help="Path to the pdf file of the paper.")
    parser.add_argument(
        "--pdf-rename-pattern",
        type=str,
        default="{title}.pdf",
        help="Pattern to rename the pdf file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to the title of the paper. Set to an empty string to not rename the pdf file.",
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
        help="Pattern to name the note file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to the same name as the (renamed) pdf file.",
    )

    args = parser.parse_args()

    return args


def commandline_entrypoint() -> None:
    args = parse_args()
    try:
        paper2note(
            args.pdf,
            args.pdf_rename_pattern if args.pdf_rename_pattern != "" else None,
            args.note_target_folder,
            args.note_template_path,
            args.note_filename_pattern,
        )
    except Exception as e:
        logger.error("An error occured.")
        logger.error(e)
