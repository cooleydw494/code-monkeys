import os

import yaml

from definitions import STORAGE_DEFAULTS_PATH, MONKEY_CONFIG_CLASS_PATH


def update_monkey_config_class():
    MONKEY_CONFIG_DEFAULTS_PATH = os.path.join(STORAGE_DEFAULTS_PATH, "monkey-config-defaults.yaml")

    with open(MONKEY_CONFIG_DEFAULTS_PATH, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    formatted_properties = [
        "    " + key + ": Optional[" + type(config[key]).__name__ + "] = field(default=None)" for key in config.keys()]

    # Format the validations
    formatted_validations = []
    for key, value in config.items():
        if isinstance(value, bool):
            formatted_validations.append(f"        self.{key} = validate_bool('{key}', self.{key})")
        elif isinstance(value, int):
            formatted_validations.append(f"        self.{key} = validate_int('{key}', self.{key})")
        elif isinstance(value, float):
            formatted_validations.append(f"        self.{key} = validate_float('{key}', self.{key})")
        elif isinstance(value, str):
            if os.path.isabs(value):
                formatted_validations.append(f"        self.{key} = validate_path('{key}', self.{key})")
            else:
                formatted_validations.append(f"        self.{key} = validate_str('{key}', self.{key})")
        elif isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                formatted_validations.append(f"        self.{key} = validate_list_str('{key}', self.{key})")
            else:
                raise ValueError(f"{key} contains non-string items")

    import re

    # Load the MonkeyConfig class
    with open(MONKEY_CONFIG_CLASS_PATH, 'r') as class_file:
        class_lines = class_file.readlines()

    props_start_index = props_end_index = validations_start_index = validations_end_index = None

    # Regular expressions for the markers
    props_start_re = re.compile(r'\[\s*MONKEY_CONFIG_PROPS_START\s*\]')
    props_end_re = re.compile(r'\[\s*MONKEY_CONFIG_PROPS_END\s*\]')
    validations_start_re = re.compile(r'\[\s*MONKEY_CONFIG_VALIDATIONS_START\s*\]')
    validations_end_re = re.compile(r'\[\s*MONKEY_CONFIG_VALIDATIONS_END\s*\]')

    for i, line in enumerate(class_lines):
        if props_start_re.search(line):
            props_start_index = i + 1
        elif props_end_re.search(line):
            props_end_index = i
        elif validations_start_re.search(line):
            validations_start_index = i + 1
        elif validations_end_re.search(line):
            validations_end_index = i

    if None in [props_start_index, props_end_index, validations_start_index, validations_end_index]:
        raise Exception("Couldn't find all markers in the class file.")

    # Add newlines to the formatted properties and validations
    formatted_properties = [p + os.linesep for p in formatted_properties]
    formatted_validations = [v + os.linesep for v in formatted_validations]

    # Replace the sections
    new_class_lines = class_lines[:props_start_index] + formatted_properties + class_lines[
                                                                               props_end_index:validations_start_index] + formatted_validations + class_lines[
                                                                                                                                                  validations_end_index:]

    # Write the updated MonkeyConfig class
    with open(MONKEY_CONFIG_CLASS_PATH, 'w') as class_file:
        class_file.write(''.join(new_class_lines))  # join the lines without adding extra newlines