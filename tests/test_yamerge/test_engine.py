from typing import Generator

from yamerge.engine import TransformerSystem, TransformerGenerator, Transformer


class AddOneTransformerGenerator(TransformerGenerator[int]):
    # pylint: disable=too-few-public-methods
    def __init__(self, max_value: int):
        self.max_value = max_value

    def match(self, obj: int) -> Generator[Transformer[int], None, None]:
        if obj < self.max_value:
            yield AddOneTransformer()


class AddOneTransformer(Transformer[int]):
    def apply(self, obj: int) -> int:
        return obj + 1


def test_engine():
    assert TransformerSystem([
        AddOneTransformerGenerator(max_value=12)
    ]).apply(5) == 12

# Todo: test precedence system
