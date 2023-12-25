import tomllib
from pathlib import Path

_prompts = {}


def set_prompt_file(path: str|Path):
    global _prompts
    with open(path, 'rb') as f:
        _prompts = tomllib.load(f)


def get_prompt(key, **variables):
    global _prompts
    if variables:
        return _prompts[key].format(**variables)
    else:
        return _prompts[key]
