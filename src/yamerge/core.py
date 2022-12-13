from typing import List, Generator, Optional, Union

YamlData = Union[dict, list, int, float, str]
YamlIndex = Union[str, int]


class YamlBackRef:
    """
    Back-Reference datastructure for YAML nodes.
    Liked list with element references of all the nodes parents up to the root.
    """
    def __init__(self, element: YamlData, index: Optional[YamlIndex], parent: Optional['YamlBackRef']):
        self.element = element
        self.index = index
        self.parent = parent

    def __repr__(self):
        return f'{self.element}@{self.index} <- {self.parent}'

    @staticmethod
    def root(element: YamlData) -> 'YamlBackRef':
        return YamlBackRef(element, None, None)


def yaml_backref_depth(br: YamlBackRef) -> int:
    """
    Find depth of a node by its backref.
    :param br: Backref
    :return: Node depth (root is 0)
    """
    depth = 0
    while br.parent is not None:
        br = br.parent
        depth += 1
    return depth


def iter_yaml_backref(br: YamlBackRef, include_current: bool = False) -> Generator[YamlBackRef, None, None]:
    """
    Iterate all parents of a backref node.
    :param br: Backref
    :param include_current: Should the input node be included.
    :return: Generator.
    """
    if include_current:
        yield br
    while br.parent is not None:
        yield br.parent
        br = br.parent


def yaml_backref_indices(br: YamlBackRef) -> List[YamlIndex]:
    """
    Find all (parent) indices of a backref
    :param br: Backref
    :return: List of indices
    """
    return list(reversed([
        br.index for br in iter_yaml_backref(br, True)
    ]))[1:]


def iter_yaml_data_bfs(root: YamlData) -> Generator[YamlBackRef, None, None]:
    """
    Simple breadth-first-search (BFS) iteration on the yaml data structure.
    Iterates all nodes off all nested lists and dicts.
    :param root: Root node
    :return: Generator.
    """
    queue: List[YamlBackRef] = [YamlBackRef.root(root)]
    while len(queue) > 0:
        current = queue.pop(0)
        yield current
        if isinstance(current.element, dict):
            queue.extend([YamlBackRef(val, key, current) for key, val in current.element.items()])
        elif isinstance(current.element, list):
            queue.extend([YamlBackRef(val, idx, current) for idx, val in enumerate(current.element)])
