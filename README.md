# Paper2Note
This is a little utility that helps to create templated notes from the pdf file of scientific papers using their autoextracted metadata.
By default the tool also renames the pdf file to the title of the paper.

The tool is based on the great [pdf2bib library](https://github.com/MicheleCotrufo/pdf2bib).


## Example Use Case
I use this tool extensively in conjuction with [logseq](https://logseq.com/) to create a knowledge base of scientific papers without any need to use separate reference management software.

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

Without any additional options, the utility will set the name of the pdf file to the title of the paper and create a markdown file in the same folder as the pdf which corresponds to [this template](paper2note/templates/reference.md).
If a file with the same name already exists, the utility will _not_ overwrite.

A couple of configuration options are available to customize the behavior of the utility.
```txt
positional arguments:
  pdf                   Path to the pdf file of the paper.

options:
  -h, --help            show this help message and exit
  --pdf-rename-pattern PDF_RENAME_PATTERN
                        Pattern to rename the pdf file. All entries of the metadata can be used as placeholders.   
                        Placeholder must be in curly braces. Defaults to the title of the paper. Set to an empty   
                        string to not rename the pdf file.
  --note-target-folder NOTE_TARGET_FOLDER
                        Folder where the note should be saved to. Can be an absolute path or relative to the       
                        directory from wich the script is called. Defaults to the directory of the pdf file.       
  --note-template-path NOTE_TEMPLATE_PATH
                        Path to the note template. Can be an absolute path or relative to the directory from wich  
                        the script is called. Defaults to a default note template.
  --note-filename-pattern NOTE_FILENAME_PATTERN
                        Pattern to name the note file. All entries of the metadata can be used as placeholders.    
                        Placeholder must be in curly braces. Defaults to the same name as the (renamed) pdf file. 
```

### Context menu
As of now, the context menu entry is only available on windows. (I am happy to accept pull requests to add this functionality for other operating systems.) 

#### Installation
The (default) command described above can also be executed by right-clicking on a pdf file and selecting the "paper2note" option. 
To enable this functionality, execute the following command in a terminal with administrator rights:
```bash
paper2note-context-menu
```

#### Removal
To remove the context menu entry, execute the following command in a terminal with administrator rights:
```bash
paper2note-context-menu --remove
```

#### Customization
If you want to customize the behavior of the context menu entry, you can pass the arguments for the `paper2note` command to the `paper2note-context-menu` command. In this case all the invocations of the context menu entry will use the passed arguments.
For example:
```bash
paper2note-context-menu '--pdf-rename-pattern "{title} - {author}" --note-target-folder "path/to/notes" --note-template-path "path/to/template.md" --note-filename-pattern "{title} - {year}"'
```

You can adapt the behavior of the context menu entry further with the following options:
```txt
positional arguments:
  arguments             The command args to configure the context menu entry with. If nothing given all the default args will be used.

options:
  -h, --help            show this help message and exit
  --entry-name ENTRY_NAME
                        The displayed name of the context menu entry.
  --remove              Remove the context menu entry instead of creating it.
  --keep-open           Keep the command prompt open after the command has been executed.
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
- `bibtex`: The full unmodified bibtex entry of the paper
- `type`: The type of the paper
- `author_i`: The i-th author of the paper were i is a number between 1 and the number of authors
- `author_last`: The last named author of the paper
- `logseq_author_listing`: A string of comma separated author names in the form [[author1]], [[author2]], ... for use in logseq
- `extraction_method`: The method used to extract the metadata from the pdf file
- `path`: The path to the (renamed) pdf file
- `relative_logseq_path`: If the pdf is located in a subdirectory of the logseq directory, this key contains the relative path to the pdf file from the logseq directory. Otherwise it is an empty string.

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