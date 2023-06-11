import os

from definitions import STOR_TEMP_PATH
from pack.modules.core.config_mgmt.monkey_config.monkey_config_class import MonkeyConfig
from pack.modules.core.theme.theme_functions import print_t, input_t, apply_t
from pack.modules.core.utils.get_monkey_name import get_monkey_name


def set_loaded_monkey(given_monkey_name: str) -> None:
    monkey_path = os.path.join(STOR_TEMP_PATH, "loaded-monkey-name.txt")
    with open(monkey_path, 'w') as file:
        file.write(given_monkey_name)


def get_loaded_monkey() -> str or None:
    monkey_path = os.path.join(STOR_TEMP_PATH, "loaded-monkey-name.txt")
    with open(monkey_path, 'r') as file:
        monkey_name = file.read()
    if monkey_name == '':
        return None
    return monkey_name


def load_monkey_config(given_monkey_name=None) -> MonkeyConfig:
    loaded_monkey_name = get_loaded_monkey()
    if loaded_monkey_name is not None and given_monkey_name is None:
        use_current = input_t(f"Continue with loaded monkey: {apply_t(loaded_monkey_name, 'important')}?", '(y/n)')
        if use_current == 'y':
            monkey_name = loaded_monkey_name
        else:
            monkey_name, _ = get_monkey_name(prompt_user=True)
    elif given_monkey_name is not None:
        monkey_name = given_monkey_name
    else:
        print_t("No monkey name or currently loaded monkey.", "quiet")
        monkey_name = get_monkey_name(prompt_user=True)

    set_loaded_monkey(monkey_name)
    return MonkeyConfig.load(monkey_name=monkey_name)
