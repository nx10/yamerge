"""
Light YAML library abstraction layer, so it can be exchanged easily in the future.
Tested with `pyyaml` and `ruamel.yaml`.
"""

from os import PathLike
from typing import Union

from ruamel.yaml import YAML

from .core import YamlData


yaml = YAML(typ='safe', pure=True)


def load_yaml_str(yaml_str: str) -> YamlData:
    return yaml.load(yaml_str)


def load_yaml_file(filename: Union[str, PathLike]) -> YamlData:
    with open(filename, 'r', encoding='utf-8') as file:
        return yaml.load(file)


def save_yaml_str(yaml_data: YamlData) -> str:
    return yaml.dump(yaml_data)


def save_yaml_file(yaml_data: YamlData, filename: Union[str, PathLike]) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(yaml_data, stream=file)
