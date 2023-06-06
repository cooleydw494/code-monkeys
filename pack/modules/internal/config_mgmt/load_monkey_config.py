import os

from definitions import STORAGE_TEMP_PATH
from pack.modules.internal.config_mgmt.monkey_config_class import MonkeyConfig
from pack.modules.internal.theme.theme_functions import print_t, input_t, apply_t
from pack.modules.internal.utils.get_monkey_name import get_monkey_name


def set_loaded_monkey(given_monkey_name: str) -> None:
    monkey_path = os.path.join(STORAGE_TEMP_PATH, "loaded-monkey-name.txt")
    with open(monkey_path, 'w') as file:
        file.write(given_monkey_name)


def get_loaded_monkey() -> str or None:
    monkey_path = os.path.join(STORAGE_TEMP_PATH, "loaded-monkey-name.txt")
    with open(monkey_path, 'r') as file:
        monkey_name = file.read()
    if monkey_name == '':
        return None
    return monkey_name


def load_monkey_config(given_monkey_name=None) -> MonkeyConfig:
    loaded_monkey_name = get_loaded_monkey()
    if loaded_monkey_name is not None and given_monkey_name is None:
        use_current = input_t(f"Currently loaded monkey: {apply_t(loaded_monkey_name, 'important')}."
                              + apply_t(" Continue with this monkey?", 'input'), '(y/n)')
        if use_current == 'y':
            return MonkeyConfig.load(monkey_name=loaded_monkey_name)
    elif given_monkey_name is None:
        print_t("No monkey name or currently loaded monkey.", "quiet")

    monkey_name, _ = get_monkey_name(given_monkey_name)
    set_loaded_monkey(monkey_name)
    return MonkeyConfig.load(monkey_name=monkey_name)
