import winreg as reg
from typing import List
import argparse
import sys
from pathlib import Path


def create_file_associated_menu(menu_name: str, parent_context_menus: List = None):
    """Create a context menu entry for a file type.
    This is a expandable element in the context menu and shows a submenu.
    It is only available for files of the specified type.

    Args:
        menu_name (str): The displayed name of the context menu entry.
        parent_context_menus (List, optional): The names of possible parent menus. Defaults to None.

    Raises:
        NotImplementedError: This method is currently not implemented.
    """
    raise NotImplementedError("This script is only for Windows.")


def create_file_associated_context_command(
    command_name: str, command: str, file_type=".pdf", parent_context_menus: List = None
):
    """Create a context menu entry for a file type.
    This is the actual command that is executed when the context menu entry is clicked.

    Args:
        command_name (str): The name of the command.
        command (str): The command that should be executed when the context menu entry is clicked.
            Note that the full path to the executable must be given, an short command like 'notepad' will not work.
        file_type (str, optional): The file type for which the context menu entry should be created. Defaults to ".pdf".
        parent_context_menus (List, optional): The names of possible parent menus. Defaults to None.
            If parent menus are given, the context menu entry will be created as a subentry of the parent menu.
            The parent menus must have been created before.
    """
    parent_context_menus = parent_context_menus or []

    # using .join is not a big help here
    parent_menu_key_prefix = ""
    for parent_menu in parent_context_menus:
        parent_menu_key_prefix += f"\\shell\\{parent_menu}"

    key_name = f"SystemFileAssociations\\{file_type}{parent_menu_key_prefix}\\shell\\{command_name}"

    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_name)
    reg.CloseKey(key)
    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, f"{key_name}\\command")
    reg.SetValue(key, "", reg.REG_SZ, command)
    reg.CloseKey(key)


def get_executable_path():
    python_folder = Path(sys.executable).parent
    if python_folder.parts[-1].lower() == "scripts":
        paper2note_executable_path = python_folder + "\pdf2bib.exe"
    else:
        paper2note_executable_path = python_folder + "\scripts\paper2note.exe"

    return paper2note_executable_path


def main():
    parser = argparse.ArgumentParser(
        description="Setup a context menu entry for paper2note."
    )

    parser.add_argument(
        "command",
        type=str,
        default=f'{get_executable_path()} "%1"',
        help="The command to be executed when the context menu entry is clicked.",
    )

    parser.add_argument(
        "file_type",
        type=str,
        default=".pdf",
        help="The file type for which the context menu entry should be created.",
    )

    args = parser.parse_args()

    create_file_associated_context_command(
        command_name="paper2note",
        command=args.command,
        file_type=args.file_type,
    )


if __name__ == "__main__":
    create_file_associated_context_command(
        "paper2note", 'C:\\Users\\mohes\\miniconda3\\Scripts\\paper2note "%1"'
    )
    print("Successfully created context menu entry for paper2note.")
