from pdf2bib import pdf2bib
from context_menu import menus


# def create_contect_menue_entry():
#     key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'SystemFileAssociations\\.pdf\\shell', 0, winreg.KEY_SET_VALUE)
#     subkey = winreg.CreateKey(key, 'Run script')
#     winreg.SetValue(subkey, '', winreg.REG_SZ, 'Run script')
#     command_key = winreg.CreateKey(subkey, 'command')
#     script_path = os.path.realpath(__file__)
#     winreg.SetValue(command_key, '', winreg.REG_SZ, f'python {script_path} "%1"')
#     winreg.CloseKey(command_key)
#     winreg.CloseKey(subkey)
#     winreg.CloseKey(key)


def install_right_click():
    if not (os.name == "nt"):
        logger.error(f"This functionality is currently implemented only for Windows.")
        return
    python_folder = path.dirname(python_path)
    if (
        python_folder[-7:].lower() == "scripts"
    ):  # This typically happens when python is installed in a virtual environment
        path_pdf2bib = python_folder + "\pdf2bib.exe"
    else:
        path_pdf2bib = python_folder + "\scripts\pdf2bib.exe"

    logger.info(
        f"Adding pdf2bib to the right-click context menu by adding keys to the system register..."
    )
    try:

        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, "Directory\shell\pdf2bib")
        reg.SetValueEx(key, "MUIVerb", 0, reg.REG_SZ, "pdf2bib")
        reg.SetValueEx(key, "subcommands", 0, reg.REG_SZ, "")
        reg.CloseKey(key)
        key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, "Directory\shell\pdf2bib\shell")
        reg.CloseKey(key)

        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT, "Directory\shell\pdf2bib\shell\pdf2bib_copybibtex"
        )
        reg.SetValue(
            key,
            "",
            reg.REG_SZ,
            "Retrieve and copy bibtex entries of all pdf files in this folder...",
        )
        reg.CloseKey(key)
        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT,
            "Directory\shell\pdf2bib\shell\pdf2bib_copybibtex\command",
        )
        reg.SetValue(key, "", reg.REG_SZ, path_pdf2bib + ' "%1" -clip -v')
        reg.CloseKey(key)

        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT, "SystemFileAssociations\.pdf\shell\pdf2bib"
        )
        reg.SetValueEx(key, "MUIVerb", 0, reg.REG_SZ, "pdf2bib")
        reg.SetValueEx(key, "subcommands", 0, reg.REG_SZ, "")
        reg.CloseKey(key)
        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT, "SystemFileAssociations\.pdf\shell\pdf2bib\shell"
        )
        reg.CloseKey(key)

        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT,
            "SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex",
        )
        reg.SetValue(
            key, "", reg.REG_SZ, "Retrieve and copy bibtex entry of this file..."
        )
        reg.CloseKey(key)
        key = reg.CreateKey(
            reg.HKEY_CLASSES_ROOT,
            "SystemFileAssociations\.pdf\shell\pdf2bib\shell\pdf2bib_copybibtex\command",
        )
        reg.SetValue(key, "", reg.REG_SZ, path_pdf2bib + ' "%1" -clip -v')
        reg.CloseKey(key)

        logger.info(f"All necessary keys were added to the system register.")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"A problem occurred when trying to add pdf2bib to the right-click context menu.\nNOTE: this functionality is only available in Windows, and it has to be installed from a terminal with administrator rights."
        )


def uninstall_right_click():
    if not (os.name == "nt"):
        logger.error(f"This functionality is currently implemented only for Windows.")
        return
    logger.info(f"Removing all keys associated to pdf2bib from the system register...")
    try:
        delete_sub_key(
            reg.HKEY_CLASSES_ROOT, "SystemFileAssociations\.pdf\shell\pdf2bib"
        )
        delete_sub_key(reg.HKEY_CLASSES_ROOT, "Directory\shell\pdf2bib")
        logger.info(f"All keys were removed.")
    except Exception as e:
        logger.error(e)
        logger.error(
            f"A problem occurred when trying to remove keys from the system registry.\nNOTE: this command needs to be executed from a terminal with administrator rights."
        )


def main():
    menus.FastCommand("paper2logseq", 'python -m paper2logseq "%1"')


if __name__ == "__main__":
    main()
