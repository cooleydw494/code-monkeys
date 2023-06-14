# from definitions import STOR_DEFAULTS_PATH, ROOT_PATH, MODULES_CONFIG_MGMT_PATH
from core.config_mgmt.env.update_env_class import update_env_class
from core.config_mgmt.monkey_config.update_monkey_config_class import update_monkey_config_class
from core.utils.monk.generate_monkeys import generate_monkeys


def regenerate_config_env_defs():

    update_env_class()

    update_monkey_config_class()

    generate_monkeys()
