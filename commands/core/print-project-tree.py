import argparse

from config.defs import ROOT_PATH
from core.utils.monk.theme.theme_functions import print_tree


def main(monk_args: argparse.Namespace = None):
    print_tree(
        start_dir=ROOT_PATH,
        exclude_dirs=['venv'],
        exclude_file_starts=['.', '_', 'TODO.md', 'README.md', 'requirements.txt', 'LICENSE'],
        title="Directory Tree",
        show_exts=True
    )