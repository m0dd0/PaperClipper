# Paper2Note
This is a little utility that helps to create templated notes from scientific papers. 
It is designed to work with papers in PDF format, and it is based on the great [pdf2bib](https://github.com/MicheleCotrufo/pdf2bib).

## Contents

## Installation
To install the package, you can use pip:
```bash
pip install git+https://github.com/m0dd0/paper2note.git
```

## Usage
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
The command described above can also be executed by right-clicking on a pdf file and selecting the "paper2note" option. To enable this functionality, you can use the following command:
```bash
paper2note-context-menu
```
This will run the command described above using the selected pdf file as an argument and the default options.
If you want to customize the behavior of the context menu, you can use the following command:
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

## Common Metdata
Common metadata entries which can be used in the `pdf_rename_pattern` and `note_filename_pattern`, as well as in the note template, are:
- title
- author
- year
TODO

## Accuracy of results
This utility uses the [pdf2bib](https://github.com/MicheleCotrufo/pdf2bib) library to extract metadata from the pdf file.
The pdf2bib library tries 5 different methods one after another to extract metadata is described on the respective github page.
For my usecase, the results were accurate in most cases, but there were also cases where the metadata was not extracted correctly.
This was especially the case for papers from the Neurips conference.
Emprically I found that one of the methods used by pdf2bib to extract metadata from the pdf file results in many false positives.
For this reason this library uses a fork of pdf2bib in which I disabled this method.
See [this issue](https://github.com/MicheleCotrufo/pdf2doi/issues/25) for more information.