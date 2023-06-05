import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ENV:
    DEFAULT_MONKEY: str = os.getenv('DEFAULT_MONKEY', 'default')
    WORK_PATH: str = os.getenv('WORK_PATH')
    FILE_TYPES_INCLUDED: str = os.getenv('FILE_TYPES_INCLUDED')
    FILEPATH_MATCH_EXCLUDED: str = os.getenv('FILEPATH_MATCH_EXCLUDED')
    FILE_SELECT_MAX_TOKENS: int = int(os.getenv('FILE_SELECT_MAX_TOKENS', 4000))
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    TEMPERATURE: float = float(os.getenv('TEMPERATURE', 1))
