# Logseq Integration - Step by Step Guide

## Prerequisites
I assume that you have python installed on your system. If not, you can download it from [here](https://www.python.org/downloads/).

By `<your logseq graph>` I refer to the folder where your logseq database is stored, i.e. the folder that contains the `logseq`, `pages`, `assets`, and `journal` folders.

## Step by Step Guide

### Step 1: Create a folder for your papers (optional)
If you want to link the pdf of your papers to your notes, the folder needs to be inside the folder of the Logseq database.
I recommend putting them somewhere into the `assets` folder, like `<your logseq graph>/assets/storages/Papers`.

### Step 2: Install the `paper2note` tool
In a terminal, run the following command to install the tool:
```bash
pip install git+https://github.com/m0dd0/paper2note.git
```

### Step 3: Setup the context menu entry
Execute the following command in a terminal with administrator rights:
```bash
paper2note-context-menu "--note-target-folder <your logseq graph>/pages"
```

### Step 4: Execute the context menu entry on a paper
Right-click on a pdf file and select the "paper2note" option.

### Step 5: Open the created note in Logseq
You will see that a note has been created in the `pages` folder of your Logseq database. 
You can now open the note in Logseq and start taking notes.

## Using your own template
If you want to use your own template for the notes, you can specify the path to the template with the `--note-template-path` option in step 3. 
The template should be a markdown file with placeholders for the metadata of the paper. 
The placeholders must be in curly braces. 
See the [README](../README.md) for more information on the available placeholders.