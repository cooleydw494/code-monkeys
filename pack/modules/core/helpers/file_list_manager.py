import os
import time
from typing import List

from definitions import STOR_TEMP_PATH, nl
from pack.modules.core.config_mgmt.monkey_config.monkey_config_class import MonkeyConfig
from pack.modules.core.gpt.token_counter import TokenCounter
from pack.modules.core.theme.theme_functions import print_t


class FileListManager:

    def __init__(self, m: MonkeyConfig):
        self.m = m
        self.include_extensions = self.m.FILE_TYPES_INCLUDED.split(',')
        self.exclude_patterns = self.m.FILEPATH_MATCH_EXCLUDED.split(',')
        self.max_tokens = self.m.FILE_SELECT_MAX_TOKENS
        self.token_counter = TokenCounter(m.MAIN_MODEL)
        self.output_file = os.path.join(STOR_TEMP_PATH, 'files-to-process.txt')

    @staticmethod
    def resolve_path(path: str) -> str:
        return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))

    def should_include(self, file_path: str) -> bool:
        return (
                any(file_path.endswith(ext) for ext in self.include_extensions) and
                not any(pattern.strip() in file_path for pattern in self.exclude_patterns)
        )

    def get_filtered_files(self):
        """Filters files by token count and returns a list of valid files."""
        filtered_files = []
        print_t("Filtering files... this might take a while depending on the size of your WORK_PATH.", 'loading')
        print_t(f'WORK_PATH: {self.m.WORK_PATH}', 'info')

        for root, _, files in os.walk(self.m.WORK_PATH):
            for file in files:
                print(".", end='', flush=True)
                time.sleep(0.001)

                if self.should_include(file):
                    absolute_path = self.resolve_path(os.path.join(root, file))
                    with open(absolute_path, 'r') as f:
                        num_tokens = self.token_counter.count_tokens(f.read())

                    if num_tokens <= self.max_tokens:
                        filtered_files.append(absolute_path)

        print_t("Filtering completed!", 'success')

        return filtered_files

    def write_files_to_process(self, filtered_files: List = None):
        if filtered_files is None:
            filtered_files = self.get_filtered_files()
        with open(self.output_file, "w") as f:
            for idx, file_path in enumerate(filtered_files, start=1):
                f.write(f"{file_path}{nl}")

        print_t(f"File list saved to {self.output_file}. Enjoy your 🐒 !", 'done')

    def select_and_remove_file(self):
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            return None
        selected_file = lines.pop(0)

        with open(self.output_file, "w") as f:
            f.writelines(lines)

        return selected_file.strip()
