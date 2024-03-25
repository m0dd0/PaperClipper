# Paper2Note
This is a little utility that helps to create templated notes from scientific papers. 
It is designed to work with papers in PDF format, and it is based on the great [pdf2bib library](https://github.com/MicheleCotrufo/pdf2bib).

## Example Use Case
I use this tool extensively in conjuction with [logseq](https://logseq.com/) to create a knowledge base of scientific papers without any need to use separate reference management software.

TODO gif here

## Contents

## Installation
To install the package, you can use pip:
```bash
pip install git+https://github.com/m0dd0/paper2note.git
```

## Usage
The tool can be used as a command line utility, as a context menu entry or as a python library.

### Command line
To create a reference note from a paper, you can use the following command:
```bash
paper2note path/to/paper.pdf
```

Without any additional options, the utility will create a markdown file in the same folder as the pdf which corresponds to [this template](paper2note/templates/reference.md).
If a file with the same name already exists, the utility will do nothing.

The utility provides also functionality to rename the pdf file according to the metadata of the paper, configure custom note templates and specify the folder where the note should be saved to:
```bash
positional arguments:
  pdf                   Path to the pdf file of the paper.

options:
  -h, --help            show this help message and exit
  --pdf-rename-pattern PDF_RENAME_PATTERN
                        Pattern to rename the pdf file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. If not provided no renaming will be executed.
  --note-target-folder NOTE_TARGET_FOLDER
                        Folder where the note should be saved to. Can be an absolute path or relative to the directory from wich the script is called. Defaults to the directory of the pdf file.
  --note-template-path NOTE_TEMPLATE_PATH
                        Path to the note template. Can be an absolute path or relative to the directory from wich the script is called. Defaults to a default note template.
  --note-filename-pattern NOTE_FILENAME_PATTERN
                        Pattern to name the note file. All entries of the metadata can be used as placeholders. Placeholder must be in curly braces. Defaults to '{title}'.
```

### Context menu
The command described above can also be executed by right-clicking on a pdf file and selecting the "paper2note" option. 
To enable this functionality, use the following command:
```bash
paper2note-context-menu
```

If you want to customize the behavior of the context menu entry, you can pass the command which should be executed when the context menu entry is clicked as an argument to the `paper2note-context-menu` command like this:
```bash
paper2note-context-menu "paper2note --pdf-rename-pattern "{title} - {author}" --note-target-folder "path/to/notes" --note-template-path "path/to/template.md" --note-filename-pattern "{title} - {author}""
```

### Python Library
The utility can also be used as a python library. 
The library contains exactly one function, `paper2note`.
The following example shows how to create a reference note from a paper:
```python
from paper2note import paper2note

paper2note("path/to/paper.pdf", pdf_rename_pattern="{title} - {author}", note_target_folder="path/to/notes", note_template_path="path/to/template.md", note_filename_pattern="{title} - {author}")
```
Have a look at the docstring of the function for more information.

## Metdata
The following keys can be used as placeholders in the `pdf_rename_pattern`, `note_filename_pattern` and the note template.
Sometimes not all metadata can be extracted from the pdf file. In this case the respective key will be filled with a placeholder string such as e.g. `<no journal found>`.
- `title`: The title of the paper
- `authors`: A string of comma separated full author names
- `year`: The year of publication
- `month`: The month of publication
- `day`: The day of publication
- `journal`: The journal in which the paper was published
- `doi`: The doi of the paper
- `url`: The url of the paper
- `volume`: The volume of the journal
- `page`: The page of the journal
- `abstract`: The abstract of the paper
- `type`: The type of the paper
- `author_i`: The i-th author of the paper were i is a number between 1 and the number of authors
- `author_last`: The last named author of the paper

## Accuracy of results
This utility uses the [pdf2bib](https://github.com/MicheleCotrufo/pdf2bib) library to extract metadata from the pdf file.
The pdf2bib library tries 5 different methods one after another to extract metadata is described on the respective github page.
For my usecase, the results were accurate in most cases, but there were also cases where the metadata was not extracted correctly.
This was especially the case for papers from the Neurips conference.
Emprically I found that one of the methods used by pdf2bib to extract metadata from the pdf file results in many false positives.
For this reason this library uses a fork of pdf2bib in which I disabled this method.
See [this issue](https://github.com/MicheleCotrufo/pdf2doi/issues/25) for more information.

## Using Environments
If you install the package into an environment like conda or venv the command line utility will only be available in this environment.
However, once you have added the context menu entry, you can use the context menu regardless of the environment you are in.

## Contribution
Feel free to open an issue or a pull request if you have any suggestions or found a bug.