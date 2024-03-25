import winreg
import argparse
import sys
from pathlib import Path
import logging
import os

logger = logging.getLogger("paper2note")


def delete_sub_key(root: str, sub: str):
    """Delete a registry key and all its subkeys.

    Args:
        root (str): The root key.
        sub (str): The subkey to be deleted.
    """
    # credits: https://stackoverflow.com/questions/38205784/python-how-to-delete-registry-key-and-subkeys-from-hklm-getting-error-5
    try:
        open_key = winreg.OpenKey(root, sub, 0, winreg.KEY_ALL_ACCESS)
        num, _, _ = winreg.QueryInfoKey(open_key)
        for _ in range(num):
            child = winreg.EnumKey(open_key, 0)
            delete_sub_key(open_key, child)
        try:
            winreg.DeleteKey(open_key, "")
        except Exception:
            logger.error(f"Failed to delete key {sub}")
        finally:
            winreg.CloseKey(open_key)
    except Exception:
        logger.error(f"Failed to open key {sub}")


def remove_file_associated_context_command(command_name: str, file_type=".pdf"):
    """Remove a context menu entry for a file type.

    Args:
        command_name (str): The name of the command.
        file_type (str, optional): The file type for which the context menu entry should be removed. Defaults to ".pdf".
    """
    key_name = f"SystemFileAssociations\\{file_type}\\shell\\{command_name}"

    delete_sub_key(winreg.HKEY_CLASSES_ROOT, key_name)


def create_file_associated_context_command(
    command_name: str, command: str, file_type=".pdf"
):
    """Create a context menu entry for a file type.
    This is the actual command that is executed when the context menu entry is clicked.

    Args:
        command_name (str): The name of the command.
        command (str): The command that should be executed when the context menu entry is clicked.
            Note that the full path to the executable must be given, an short command like 'notepad' will not work.
        file_type (str, optional): The file type for which the context menu entry should be created. Defaults to ".pdf".
    """

    key_name = f"SystemFileAssociations\\{file_type}\\shell\\{command_name}"

    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_name)
    winreg.CloseKey(key)
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_name}\\command")
    winreg.SetValue(key, "", winreg.REG_SZ, command)
    winreg.CloseKey(key)


def get_executable_path() -> str:
    """Get the path to the paper2note executable.

    This is necessary to create a context menu entry as the command must be an absolute path.
    Also accounts for the case when the script is executed from a virtual environment.

    Returns:
        str: The path to the paper2note executable.
    """

    python_folder = Path(sys.executable).parent
    if python_folder.parts[-1].lower() == "scripts":
        paper2note_executable_path = python_folder / "pdf2bib.exe"
    else:
        paper2note_executable_path = python_folder / "scripts" / "paper2note.exe"

    return str(paper2note_executable_path)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Setup a context menu entry for paper2note."
    )

    parser.add_argument(
        "--command-args",
        type=str,
        default="",
        help="The command args to configure the context menu entry with. If nothing given all the default args will be used.",
    )

    parser.add_argument(
        "--entry-name",
        type=str,
        default="paper2note",
        help="The displayed name of the context menu entry.",
    )

    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the context menu entry instead of creating it.",
    )

    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep the command prompt open after the command has been executed.",
    )

    args = parser.parse_args()

    return args


def commandline_entrypoint():
    args = parse_args()

    if not os.name == "nt":
        raise NotImplementedError("This script is only implemented for Windows.")

    if args.remove:
        remove_file_associated_context_command(args.entry_name)
        logger.info(f"Context menu entry '{args.entry_name}' removed.")
    else:
        command = f'{"cmd /k " if args.keep_open else ""}{get_executable_path()} "%1" {args.command_args}'
        create_file_associated_context_command(
            command_name=args.entry_name, command=command
        )
        logger.info(
            f"Context menu entry '{args.entry_name}' created for command '{command}'."
        )
