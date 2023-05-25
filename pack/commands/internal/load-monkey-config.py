import os
import sys

from definitions import MONKEYS_PATH
from pack.modules.custom.style.visuals import printc

# Check if the monkey name argument is provided
if len(sys.argv) < 2:
    printc("Please provide the name of the monkey as a command-line argument.", "important")
    sys.exit(1)

# Get the monkey name from the command-line argument
monkey_name = sys.argv[1]
monkey_file = os.path.join(MONKEYS_PATH, monkey_name)

# Check if the monkey configuration file exists
if not os.path.isfile(monkey_file):
    printc(f"Monkey config file '{monkey_name}.py' not found.", "error")
    sys.exit(1)

# Load the monkey configuration variables
monkey_config = {}
try:
    exec(open(monkey_file).read(), monkey_config)
except Exception as e:
    printc(f"Failed to load monkey config from file: '{monkey_name}'. Error: {str(e)}", "error")
    sys.exit(1)

# Extract the configuration variables
main_prompt = monkey_config.get("MAIN_PROMPT", "")
usage_prompt = monkey_config.get("USAGE_PROMPT", "")
summary_prompt = monkey_config.get("SUMMARY_PROMPT", "")
special_file = monkey_config.get("SPECIAL_FILE", "")
default_monkey = monkey_config.get("DEFAULT_MONKEY", "")
summary_model = monkey_config.get("SUMMARY_MODEL", "")
main_model = monkey_config.get("MAIN_MODEL", "")
usage_model = monkey_config.get("USAGE_MODEL", "")

# Print the loaded configuration variables
printc("🐒 Monkey Configuration Loaded 🐒", 'success')
printc("Monkey Name: ", 'cyan') + f"{monkey_name}"
printc("Main Prompt: ", 'cyan') + f"{main_prompt}"
printc("Usage Prompt: ", 'cyan') + f"{usage_prompt}"
printc("Summarization Prompt: ", 'cyan') + f"{summary_prompt}"
printc("Special File: ", 'cyan') + f"{special_file}"
printc("Default Monkey: ", 'cyan') + f"{default_monkey}"
printc("Summarization Model: ", 'cyan') + f"{summary_model}"
printc("Main Prompt Model: ", 'cyan') + f"{main_model}"
printc("Usage Prompt Model: ", 'cyan') + f"{usage_model}"
