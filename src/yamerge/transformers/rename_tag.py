from typing import Generator

from yamerge.engine import Transformer, TransformerGenerator
from ..core import YamlData, iter_yaml_data_bfs


class RenameTagTransformer(Transformer[YamlData]):
    def __init__(self, generator: 'RenameTagTransformerGenerator', tag_dict: dict):
        self.generator = generator
        self.tag_dict = tag_dict

    def precedence(self) -> int:
        return self.generator.precedence

    def apply(self, obj: YamlData) -> YamlData:
        self.tag_dict[self.generator.rename_to] = self.tag_dict.pop(self.generator.rename_from)
        return obj


class RenameTagTransformerGenerator(TransformerGenerator[YamlData]):
    # pylint: disable=too-few-public-methods
    def __init__(self, rename_from: str, rename_to: str, precedence: int = 0):
        self.rename_from = rename_from
        self.rename_to = rename_to
        self.precedence = precedence

    def match(self, obj: YamlData) -> Generator[YamlData, None, None]:
        for br in iter_yaml_data_bfs(obj):
            if isinstance(br.element, dict) and self.rename_from in br.element:
                yield RenameTagTransformer(self, br.element)
