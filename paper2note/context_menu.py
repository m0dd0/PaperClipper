import winreg as reg
import argparse
import sys
from pathlib import Path
import logging

logger = logging.getLogger("paper2note")


def remove_file_associated_context_command(command_name: str, file_type=".pdf"):
    """Remove a context menu entry for a file type.

    Args:
        command_name (str): The name of the command.
        file_type (str, optional): The file type for which the context menu entry should be removed. Defaults to ".pdf".
    """

    key_name = f"SystemFileAssociations\\{file_type}\\shell\\{command_name}"
    reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_name)
    # TODO test


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

    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_name)
    reg.CloseKey(key)
    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, f"{key_name}\\command")
    reg.SetValue(key, "", reg.REG_SZ, command)
    reg.CloseKey(key)


def get_executable_path() -> str:
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
        "--command",
        type=str,
        default=f'paper2note "%1"',
        help="The command to be executed when the context menu entry is clicked. Use '%1' as a placeholder for the file path.",
    )

    parser.add_argument(
        "--file_type",
        type=str,
        default=".pdf",
        help="The file type for which the context menu entry should be created.",
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

    # TODO check for OS

    if args.remove:
        raise NotImplementedError(
            "The removal of context menu entries is not yet implemented."
        )
        # TODO implement
    else:
        args.command = args.command.replace("paper2note", get_executable_path())
        args.command = f"{'cmd /k' if args.keep_open else ''} {args.command}"
        create_file_associated_context_command(
            command_name=args.entry_name,
            command=args.command,
            file_type=args.file_type,
        )
        logger.info(
            f"Context menu entry '{args.entry_name}' for file type '{args.file_type}' created."
        )
