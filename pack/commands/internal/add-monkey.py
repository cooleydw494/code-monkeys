import os
import sys

from ruamel.yaml import YAML

from definitions import ROOT_PATH
from pack.modules.custom.theme.theme_functions import print_t, input_t
from pack.modules.internal.utils.general_helpers import get_monkey_config_defaults

yaml = YAML()
MONKEY_CONFIG_DEFAULTS = get_monkey_config_defaults(short=True)

# Define input prompts
INPUT_PROMPTS = {
    'MAIN_PROMPT': "Please generate code for the following task",
    'SUMMARY_PROMPT': "Provide a summary of this file",
    'MAIN_PROMPT_ULTIMATUM': "Limit your response to the full contents of a python script, and nothing else.",
    'WORK_PATH': "Please enter the path to the the directory you'd like to work in",
    'OUTPUT_EXAMPLE': "Limit your output strictly to the contents of the file, like this: ```complete contents of "
                      "file```",
    'OUTPUT_CHECK_PROMPT': "Examine the following output and determine if 1. The output is complete and 2. The output "
                           "is limited strictly to the contents of a file. Format your response exactly like this: "
                           "```is_limited_to_file_contents:[1/0],is_complete:[1/0]```.",
    'OUTPUT_FILENAME_APPEND': "Please enter text to append to output filenames:",
    'OUTPUT_EXT': "Please enter text to override output file extensions",
    'SPECIAL_FILE': "Please enter a file which will be summarized using SUMMARY_PROMPT to give context for the main "
                    "prompt (absolute path)",
    'MAIN_MODEL': "Enter the model to use for the main prompts. Choose 3 (gpt-3.5-turbo) or 4 (gpt-4)",
    'SUMMARY_MODEL': "Enter the model to use for the summary prompts. Choose 3 (gpt-3.5-turbo) or 4 (gpt-4)",
    'OUTPUT_CHECK_MODEL': "Enter the model to use for the usage prompts. Choose 3 (gpt-3.5-turbo) or 4 (gpt-4)",
    'MAIN_TEMP': "Enter the temperature to use for the main prompts (a value between 0 and 1)",
    'SUMMARY_TEMP': "Enter the temperature to use for the summary prompts (a value between 0 and 1)",
    'OUTPUT_CHECK_TEMP': "Enter the temperature to use for the usage prompts (a value between 0 and 1)"
}


def is_valid_path():
    while True:
        path = input_t("Please enter the path: ", "(absolute path or you can use ~ on Mac/Linux)")
        absolute_path = os.path.expanduser(path)
        if os.path.exists(absolute_path):
            return str(absolute_path)
        else:
            print_t("Invalid path. Please try again.", 'error')


def handle_input(prop_name, description):
    input_handlers = {
        'path': lambda p, d: is_valid_path(),
        'model': lambda p, d: input_t(p, d) if input_t(p, d) in ['3', '4'] else '4',
        'default': lambda p, d: input_t(p, d)
    }
    prop_lower = prop_name.lower()
    input_type = 'path' if 'path' in prop_lower else 'model' if 'model' in prop_lower else 'default'
    return input_handlers[input_type](prop_name, description)


def handle_yaml(data):
    return {key: handle_input(key, value) for key, value in data.items()}


def main(monkey_name=None):
    # if monkey_name is '', loop until a valid name is provided
    while not monkey_name:
        monkey_name = input_t("Please enter a name for your monkey: ", '(letters and hyphens only)')
        # only allow letters and hyphens in monkey names
        if ' ' in monkey_name or not monkey_name.replace('-', '').isalpha():
            print_t("Invalid name. Please try again.", 'error')
            monkey_name = ''
        else:
            break

    print_t(f"Let's configure your new {monkey_name} monkey", 'monkey')

    with open(os.path.join(ROOT_PATH, 'monkey-manifest.yaml'), 'r') as file:
        # Use yaml object instead of yaml.safe_load to load the data
        monkey_manifest = yaml.load(file)

    if monkey_name in monkey_manifest.keys():
        print_t(f"A monkey named {monkey_name} already exists.", 'important')
        result = input_t(f"Would you like to overwrite the existing config?", '(y/n)')
        if result.lower() != 'y':
            sys.exit(0)
        else:
            print_t("Continuing configuration...", 'done')

    new_monkey_data = handle_yaml(INPUT_PROMPTS)

    with open(os.path.join(ROOT_PATH, 'monkey-manifest.yaml'), 'w') as file:
        if monkey_name not in monkey_manifest.keys():
            file.write(os.linesep)
        monkey_manifest[monkey_name] = new_monkey_data
        # Use yaml object instead of yaml.dump to save the data
        yaml.dump(monkey_manifest, file)

    print_t("Configuration complete. The 'monkey-manifest.yaml' file has been updated.", 'done')
    print_t("Please run `monk generate-monkeys` to complete the configuration process.", 'tip')


if __name__ == '__main__':
    main()
