import dataclasses
import os
from dataclasses import dataclass

from definitions import MONKEYS_PATH
from pack.modules.internal.config_mgmt.env.env_class import ENV
from pack.modules.internal.config_mgmt.yaml_helpers import get_monkey_config_defaults
from pack.modules.internal.theme.theme_functions import print_t


@dataclass
class MonkeyConfig:
    _instance = None

    """ MONKEY_CONFIG_PROPS - DO NOT MODIFY
        Definitions of MonkeyConfig props, generated from monkey-config-defaults. """
    # [MONKEY_CONFIG_PROPS_START]
    from types import NoneType
    from typing import Optional

    from ruamel.yaml.scalarfloat import ScalarFloat
    from dataclasses import field
    FILE_TYPES_INCLUDED: Optional[str] = field(default=None)
    FILEPATH_MATCH_EXCLUDED: Optional[str] = field(default=None)
    MAX_TOKENS: Optional[int] = field(default=None)
    FILE_SELECT_MAX_TOKENS: Optional[int] = field(default=None)
    SPECIAL_FILE_PATH: Optional[str] = field(default=None)
    WORK_PATH: Optional[str] = field(default=None)
    MAIN_PROMPT: Optional[str] = field(default=None)
    SUMMARY_PROMPT: Optional[str] = field(default=None)
    MAIN_PROMPT_ULTIMATUM: Optional[str] = field(default=None)
    CHECK_OUTPUT: Optional[bool] = field(default=None)
    OUTPUT_TRIES_LIMIT: Optional[int] = field(default=None)
    OUTPUT_EXAMPLE: Optional[str] = field(default=None)
    OUTPUT_CHECK_PROMPT: Optional[str] = field(default=None)
    OUTPUT_PATH: Optional[str] = field(default=None)
    OUTPUT_EXT: Optional[str] = field(default=None)
    OUTPUT_FILENAME_APPEND: Optional[str] = field(default=None)
    OUTPUT_REMOVE_STRINGS: Optional[str] = field(default=None)
    MAIN_MODEL: Optional[int] = field(default=None)
    SUMMARY_MODEL: Optional[int] = field(default=None)
    OUTPUT_CHECK_MODEL: Optional[int] = field(default=None)
    MAIN_TEMP: Optional[ScalarFloat] = field(default=None)
    SUMMARY_TEMP: Optional[ScalarFloat] = field(default=None)
    OUTPUT_CHECK_TEMP: Optional[ScalarFloat] = field(default=None)
    # [MONKEY_CONFIG_PROPS_END]

    ENV: Optional[ENV] = field(default=None)

    def __post_init__(self):
        # print_t(f"Loaded MonkeyConfig: {self.__dict__}", 'info')

        """ MONKEY_CONFIG_VALIDATIONS - DO NOT MODIFY
        Set MonkeyConfig props with validations, generated from monkey-config-defaults & monkey_config_validations. """
        # [MONKEY_CONFIG_VALIDATIONS_START]
        from pack.modules.internal.config_mgmt.monkey_config.monkey_config_validations import validate_str, validate_bool, validate_int, validate_float, validate_path, validate_list_str
        self.FILE_TYPES_INCLUDED = validate_str('FILE_TYPES_INCLUDED', self.FILE_TYPES_INCLUDED)
        self.FILEPATH_MATCH_EXCLUDED = validate_str('FILEPATH_MATCH_EXCLUDED', self.FILEPATH_MATCH_EXCLUDED)
        self.MAX_TOKENS = validate_int('MAX_TOKENS', self.MAX_TOKENS)
        self.FILE_SELECT_MAX_TOKENS = validate_int('FILE_SELECT_MAX_TOKENS', self.FILE_SELECT_MAX_TOKENS)
        self.SPECIAL_FILE_PATH = validate_path('SPECIAL_FILE_PATH', self.SPECIAL_FILE_PATH)
        self.WORK_PATH = validate_path('WORK_PATH', self.WORK_PATH)
        self.MAIN_PROMPT = validate_str('MAIN_PROMPT', self.MAIN_PROMPT)
        self.SUMMARY_PROMPT = validate_str('SUMMARY_PROMPT', self.SUMMARY_PROMPT)
        self.MAIN_PROMPT_ULTIMATUM = validate_str('MAIN_PROMPT_ULTIMATUM', self.MAIN_PROMPT_ULTIMATUM)
        self.CHECK_OUTPUT = validate_bool('CHECK_OUTPUT', self.CHECK_OUTPUT)
        self.OUTPUT_TRIES_LIMIT = validate_int('OUTPUT_TRIES_LIMIT', self.OUTPUT_TRIES_LIMIT)
        self.OUTPUT_EXAMPLE = validate_str('OUTPUT_EXAMPLE', self.OUTPUT_EXAMPLE)
        self.OUTPUT_CHECK_PROMPT = validate_str('OUTPUT_CHECK_PROMPT', self.OUTPUT_CHECK_PROMPT)
        self.OUTPUT_PATH = validate_path('OUTPUT_PATH', self.OUTPUT_PATH)
        self.OUTPUT_EXT = validate_str('OUTPUT_EXT', self.OUTPUT_EXT)
        self.OUTPUT_FILENAME_APPEND = validate_str('OUTPUT_FILENAME_APPEND', self.OUTPUT_FILENAME_APPEND)
        self.OUTPUT_REMOVE_STRINGS = validate_str('OUTPUT_REMOVE_STRINGS', self.OUTPUT_REMOVE_STRINGS)
        self.MAIN_MODEL = validate_int('MAIN_MODEL', self.MAIN_MODEL)
        self.SUMMARY_MODEL = validate_int('SUMMARY_MODEL', self.SUMMARY_MODEL)
        self.OUTPUT_CHECK_MODEL = validate_int('OUTPUT_CHECK_MODEL', self.OUTPUT_CHECK_MODEL)
        self.MAIN_TEMP = validate_float('MAIN_TEMP', self.MAIN_TEMP)
        self.SUMMARY_TEMP = validate_float('SUMMARY_TEMP', self.SUMMARY_TEMP)
        self.OUTPUT_CHECK_TEMP = validate_float('OUTPUT_CHECK_TEMP', self.OUTPUT_CHECK_TEMP)
        # [MONKEY_CONFIG_VALIDATIONS_END]

        self.ENV = ENV()

    @classmethod
    def load(cls, monkey_name: str) -> 'MonkeyConfig':
        from pack.modules.internal.config_mgmt.yaml_helpers import read_yaml_file

        if cls._instance is None:
            monkey_path = os.path.join(MONKEYS_PATH, f"{monkey_name}.yaml")

            if not os.path.exists(monkey_path):
                raise FileNotFoundError(f"Monkey configuration file {monkey_path} not found.")

            monkey_dict = read_yaml_file(monkey_path, ruamel=True)
            monkey_dict = cls.filter_config_values(monkey_dict)
            monkey_dict = cls.apply_defaults(monkey_dict)

            cls._instance = MonkeyConfig(**monkey_dict)

        return cls._instance

    @classmethod
    def apply_default_and_validate(cls, data: dict):
        """
        Validate the provided dictionary with MonkeyConfig and return it.
        """

        data = cls.filter_config_values(data)
        data = cls.apply_defaults(data)

        # Create an instance of MonkeyConfig to perform validation
        try:
            validated_config = cls(**data)
        except (TypeError, ValueError) as e:
            print_t(f"MonkeyConfig Validation - {e}", 'error')
            exit()

        data = validated_config.__dict__
        data.pop('ENV', None)

        return data

    @classmethod
    def filter_config_values(cls, config_values: dict) -> dict:
        # Get dictionary of MonkeyConfig properties
        config_properties = {f.name for f in dataclasses.fields(cls)}
        config_properties.remove('ENV')

        # Remove any keys from data that aren't properties of the MonkeyConfig class
        config_values = {k: v for k, v in config_values.items() if k in config_properties}

        return config_values

    @classmethod
    def apply_defaults(cls, config_values: dict) -> dict:
        """
        Apply default values to the provided dictionary with MonkeyConfig and return it.
        If a value is set to None, it will be maintained as None.
        If a value isn't present, it will be set to the default value.
        :param config_values: dict
        :return: dict
        """

        # Get dictionary of MonkeyConfig properties so we don't default to env vars that aren't properties
        config_properties = {f.name for f in dataclasses.fields(cls)}
        config_properties.remove('ENV')

        env = ENV()

        for attribute in env.__annotations__:
            if attribute in config_properties and config_values.get(attribute, '**unset') == '**unset'\
                    and getattr(env, attribute, None) is not None:
                config_values[attribute] = getattr(env, attribute)

        monkey_config_defaults = get_monkey_config_defaults()
        for attribute in monkey_config_defaults:
            if config_values.get(attribute, '**unset') == '**unset' and monkey_config_defaults[attribute] is not None:
                config_values[attribute] = monkey_config_defaults[attribute]

        return config_values

