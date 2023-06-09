import os
import sys

from codemonkeys.utils.defs_utils import find_project_root, import_class_from_path_with_fallback
from codemonkeys.utils.defs_utils import get_python_command

"""  PREDEFINED FRAMEWORK INSTANCE PATHS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

ROOT_PATH = find_project_root()

AUTOMATIONS_PATH = os.path.join(ROOT_PATH, "automations")
BARRELS_PATH = os.path.join(ROOT_PATH, "barrels")
COMPOSABLES_PATH = os.path.join(ROOT_PATH, "composables")
ABILITIES_PATH = os.path.join(ROOT_PATH, "abilities")
COMMANDS_PATH = os.path.join(ROOT_PATH, "commands")

ENV_PATH = os.path.join(ROOT_PATH, ".env")
CONFIG_PATH = os.path.join(ROOT_PATH, "config")
MONKEY_MANIFEST_PATH = os.path.join(CONFIG_PATH, 'monkey-manifest.yaml')
MONKEY_CONFIG_DEFAULTS_PATH = os.path.join(CONFIG_PATH, 'monkey-config-defaults.yaml')

FRAMEWORK_CONFIG_PATH = os.path.join(CONFIG_PATH, 'framework')
THEME_CONFIG_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, 'theme.py')
ENV_CLASS_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, "env_class.py")
MONKEY_CONFIG_CLASS_PATH = os.path.join(FRAMEWORK_CONFIG_PATH, "monkey_config_class.py")

STOR_PATH = os.path.join(ROOT_PATH, "stor")
TEMP_PATH = os.path.join(STOR_PATH, "temp")

MONKEYS_PATH = os.path.join(TEMP_PATH, 'monkeys')

"""  'GLOBAL' HELPERS/VARIABLES
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

ENABLE_RELATIVE_IMPORTS = sys.path.append(ROOT_PATH)

# GET user's available Python command
PYTHON_COMMAND = get_python_command()

TOKEN_UNCERTAINTY_BUFFER = 10

# OS-agnostic newline characters
nl = os.linesep
nl2 = nl * 2


# prop or empty string helper
def _or(obj_or_class_prop, default=''):
    try:
        return obj_or_class_prop
    except AttributeError:
        return default


def import_monkey_config_class():
    from codemonkeys.config.monkey_config_class import MonkeyConfig as DefaultMonkeyConfigClass
    return import_class_from_path_with_fallback(MONKEY_CONFIG_CLASS_PATH, 'MonkeyConfig', DefaultMonkeyConfigClass)


def import_env_class():
    from codemonkeys.config.env_class import Env as DefaultEnvClass
    return import_class_from_path_with_fallback(ENV_CLASS_PATH, 'Env', DefaultEnvClass)
