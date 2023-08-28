import os
import tomllib

_prompts = {}


def prompt(key, **variables):
    global _prompts
    if not _prompts:
        path = os.path.join(os.path.dirname(__file__), 'prompts.toml')
        with open(path, 'rb') as f:
            _prompts = tomllib.load(f)
    if variables:
        return _prompts[key].format(**variables)
    else:
        return _prompts[key]
