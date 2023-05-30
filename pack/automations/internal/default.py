import json
import os
import subprocess
import sys

import openai

from definitions import PYTHON_COMMAND
from pack.modules.custom.process_file import process_file
from pack.modules.custom.summarize_special_file import summarize_special_file
from pack.modules.custom.theme.theme_functions import print_t
from pack.modules.internal.get_gpt_client import instantiate_gpt_models
from pack.modules.internal.get_monkey_name import get_monkey_name


def check_env_vars():
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY is not set.")
        work_path = os.getenv("WORK_PATH")
        if work_path is None:
            raise ValueError("WORK_PATH is not set.")
    except ValueError as error:
        print_t(f"{error}", "error")
        sys.exit(1)
    return work_path


def load_monkey_config(argv):
    monkey_name, monkey_config_file = get_monkey_name(argv)
    script_path = "../../commands/internal/load-monkey-config.py"
    process = subprocess.run([PYTHON_COMMAND, script_path, monkey_config_file], check=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    if process.returncode != 0:
        print_t(process.stderr.decode(), 'error')
        sys.exit(1)
    return json.loads(process.stdout.decode())


def main():
    # Check command-line arguments
    if len(sys.argv) < 2:
        print_t("Please provide the name of the monkey as a command-line argument.", "yellow")
        sys.exit(1)

    print_t("Welcome to the Monkeyspace! Let's wreak the opposite of havoc on your [whatever]!", "start")

    # Check and load environment variables
    work_path = check_env_vars()

    # Load monkey config
    monkey = load_monkey_config(sys.argv)

    # Instantiate necessary GPT models
    gpt_models = instantiate_gpt_models(monkey['MAIN_MODEL'], monkey['SUMMARY_MODEL'], monkey['USAGE_MODEL'])

    def gpt_client(model_name):
        return gpt_models.get(model_name)

    # Check if the special file exists
    if not os.path.isfile(monkey['SPECIAL_FILE']):
        print_t(f"Special file '{monkey['SPECIAL_FILE']}' not found.", "error")
        sys.exit(1)

    # Summarize the special file
    special_file_summary = summarize_special_file(monkey['SPECIAL_FILE'], monkey['SUMMARY_MODEL'],
                                                  monkey['SUMMARY_PROMPT'], gpt_client)
    print_t("Special file summarized successfully!", 'success')
    print_t(f"Summary:\n{special_file_summary}", 'file')

    # Iterate over each file in the work_path
    for root, dirs, files in os.walk(work_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, monkey['USAGE_PROMPT'], special_file_summary, monkey['USAGE_MODEL'],
                         monkey['MAIN_PROMPT'], monkey['MAIN_MODEL'], gpt_client)


if __name__ == '__main__':
    main()
