import winreg as reg
from sys import executable as python_path
from typing import List
import argparse


def create_file_associated_menu(menu_name: str, parent_context_menus: List = None):
    raise NotImplementedError("This script is only for Windows.")


def create_file_associated_context_command(
    command_name: str, command: str, file_type=".pdf", parent_context_menus: List = None
):
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


def main():
    parser = argparse.ArgumentParser(
        description="Setup a context menu entry for paper2note."
    )

    parser.add_argument(
        "command",
        type=str,
        help="The command to be executed when the context menu entry is clicked.",
    )

    parser.add_argument(
        "file_type",
        type=str,
        help="The file type for which the context menu entry should be created.",
    )

    parser.add_argument(
        "--parent_context_menus",
        type=str,
        nargs="+",
        help="The parent context menus under which the entry should be created.",
    )

    args = parser.parse_args()

    create_file_associated_context_command(
        command_name="paper2note",
        command=args.command,
        file_type=args.file_type,
        parent_context_menus=args.parent_context_menus,
    )


if __name__ == "__main__":
    create_file_associated_context_command(
        "paper2note", 'C:\\Users\\mohes\\miniconda3\\Scripts\\paper2note "%1"'
    )
    print("Successfully created context menu entry for paper2note.")
