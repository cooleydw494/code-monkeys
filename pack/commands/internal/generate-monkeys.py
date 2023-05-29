import os
import shutil
import time

import yaml
from definitions import MONKEYS_PATH
from pack.modules.custom.theme.theme_functions import print_t
from pack.modules.internal.utils.general_helpers import get_monkey_config_defaults


def main():
    print_t("Generating monkey configs...", 'start')
    monkey_manifest = os.path.join(MONKEYS_PATH, "monkey-manifest.yaml")
    try:
        with open(monkey_manifest, "r") as f:
            monkeys = yaml.safe_load(f)
        print_t("monkey-manifest.yaml located", 'info')
    except FileNotFoundError:
        print_t(f"Could not find monkey-manifest.yaml file. File expected to exist at {monkey_manifest}", 'error')
        return

    default_config = get_monkey_config_defaults()

    # Create the directories and configuration files
    for monkey_name, config in monkeys.items():
        print_t(f"Checking {monkey_name}", 'special')
        # Create the directory for the monkey if it doesn't exist
        monkey_dir = os.path.join(MONKEYS_PATH, monkey_name)
        os.makedirs(monkey_dir, exist_ok=True)

        # Merge the default configuration with the monkey's own configuration
        merged_config = default_config.copy()  # Start with the defaults
        merged_config.update(config)  # Overwrite with the monkey's specific config

        config_file_path = os.path.join(monkey_dir, f'{monkey_name}.yaml')
        # Check if new config content is different from the existing one
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as f:
                existing_config = yaml.safe_load(f)
            if existing_config == merged_config:
                print_t(f"Skipping {monkey_name} (no changes).", 'quiet')
                continue
            else:
                print_t(f"Changes detected for {monkey_name}. Backing up existing config.", 'info')
                os.makedirs(os.path.join(monkey_dir, 'history'), exist_ok=True)
                timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
                shutil.move(config_file_path, os.path.join(monkey_dir, 'history', f'{timestamp}.yaml'))

        # Write the config file
        with open(os.path.join(monkey_dir, f'{monkey_name}.yaml'), "w") as f:
            yaml.safe_dump(merged_config, f, default_flow_style=False)
        print_t(f"Updated config for {monkey_name}.", 'info')

    print_t("All monkeys processed successfully. Exiting.", 'done')


if __name__ == "__main__":
    main()
