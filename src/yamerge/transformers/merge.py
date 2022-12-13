import pathlib as pl
from abc import ABC, abstractmethod
from os import PathLike
from typing import Optional, List, Generator, Union

from yamerge.engine import Transformer, TransformerGenerator
from ..core import YamlData, yaml_backref_indices, yaml_backref_depth, iter_yaml_data_bfs, YamlBackRef
from ..yaml_access import load_yaml_file


def _merge_dicts(a: dict, b: dict):
    """
    Merges two arbitrarily nested dicts recursively so that
    `a` gets expanded by all values in `b` that do not exist in `a`.
    :param a: Dict
    :param b: Dict
    :return: a for chaining
    """
    for key, val in a.items():
        if isinstance(val, dict):
            b_val = b.get(key, None)
            if isinstance(b_val, dict):
                _merge_dicts(a[key], b_val)

    for key, val in b.items():
        if key not in a:
            a[key] = val

    return a


def _find_file_in_paths(file: Union[str, PathLike], paths: List[Union[str, PathLike]]) -> Optional[PathLike]:
    """
    Return the first existing file path from multiple possible locations.
    :param file: File
    :param paths: List of potential paths
    :return: Joined file path
    """
    for search_path in paths:
        candidate = pl.Path(search_path) / file
        if candidate.exists():
            return candidate
    return None


class MergeTransformer(Transformer[YamlData], ABC):
    def __init__(self, generator: 'MergeTransformerGenerator', br: YamlBackRef):
        self.generator = generator
        self.br = br
        self.depth = yaml_backref_depth(br)

    def precedence(self) -> int:
        return self.generator.base_precedence + self.depth

    def apply(self, obj: YamlData) -> YamlData:
        merge_filename = self.br.element[self.generator.merge_tag_name]
        del self.br.element[self.generator.merge_tag_name]

        assert isinstance(merge_filename, str)

        merge_filepath = _find_file_in_paths(merge_filename, self.generator.paths)
        if merge_filepath is None:
            raise Exception(f'File not found: {merge_filename}')

        merge_yaml = load_yaml_file(merge_filepath)

        self._merge(obj, merge_yaml, self.br)

        return obj

    @abstractmethod
    def _merge(self, a: YamlData, b: YamlData, a_br: Optional[YamlBackRef] = None):
        pass


class MergeTransformerGenerator(TransformerGenerator[YamlData], ABC):
    # pylint: disable=too-few-public-methods
    def __init__(
            self,
            merge_tag_name: str,
            paths: Optional[List[str]] = None,
            base_precedence: int = 1000,
            max_apply: int = 1000
    ):
        self.merge_tag_name = merge_tag_name
        self.paths = ['.'] if paths is None else paths
        self.base_precedence = base_precedence
        self.max_apply = max_apply
        self.num_apply = 0

    def match(self, obj: YamlData) -> Generator[MergeTransformer, None, None]:
        for br in iter_yaml_data_bfs(obj):
            if isinstance(br.element, dict) and self.merge_tag_name in br.element.keys():
                if self.num_apply > self.max_apply:
                    raise Exception('Maximum number of merges reached. (Infinite recursion?)')
                self.num_apply += 1
                yield self._make_transformer(
                    generator=self,
                    br=br
                )

    @abstractmethod
    def _make_transformer(self, generator: 'MergeTransformerGenerator', br: YamlBackRef) -> MergeTransformer:
        pass


class AbsoluteMergeTransformer(MergeTransformer):
    def _merge(self, a: YamlData, b: YamlData, a_br: Optional[YamlBackRef] = None):
        a_br: YamlBackRef = YamlBackRef.root(a) if a_br is None else a_br

        parent_keys = yaml_backref_indices(a_br)

        # Index overload-graph repeatedly until at base_node
        b_node = b
        for key in parent_keys:
            if not isinstance(key, str):
                raise Exception('Absolute-merge does not work nested in lists')

            if key not in b_node:
                raise Exception('Absolute-merge: Graph mismatch')

            b_node = b_node[key]

        _merge_dicts(a_br.element, b_node)

        return a


class AbsoluteMergeTransformerGenerator(MergeTransformerGenerator):
    # pylint: disable=too-few-public-methods
    def _make_transformer(self, generator: MergeTransformerGenerator, br: YamlBackRef) -> MergeTransformer:
        return AbsoluteMergeTransformer(
            generator=generator,
            br=br
        )


class RelativeMergeTransformer(MergeTransformer):
    # pylint: disable=too-few-public-methods
    def _merge(self, a: YamlData, b: YamlData, a_br: Optional[YamlBackRef] = None):
        a_br: YamlBackRef = YamlBackRef.root(a) if a_br is None else a_br
        _merge_dicts(a_br.element, b)
        return a


class RelativeMergeTransformerGenerator(MergeTransformerGenerator):
    # pylint: disable=too-few-public-methods
    def _make_transformer(self, generator: MergeTransformerGenerator, br: YamlBackRef) -> MergeTransformer:
        return RelativeMergeTransformer(
            generator=generator,
            br=br
        )
