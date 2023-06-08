import platform
import shutil
import time

from pack.modules.internal.theme.theme_functions import print_t


def main():
    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Determine the platform
    system = platform.system()
    if system == "Darwin" or system == "Linux":
        archive_format = "gztar"
    else:
        archive_format = "zip"

    # Define the files and directories to include in the archive
    files_to_export = [
        "main.py",
        "monkeys/monkey-manifest.yaml"
    ]
    directory_to_export = "backups/main"

    # Create the export archive
    export_filename = f"export-{timestamp}.{archive_format}"
    shutil.make_archive(export_filename, archive_format, "", files_to_export, directory_to_export)

    print_t(f"Export created: {export_filename}", 'done')
