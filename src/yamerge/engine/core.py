from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Generator, Iterable

T = TypeVar('T')


class Transformer(ABC, Generic[T]):
    """
    Abstract class. Transforms a data structure and reports its precedence for comparison with other transformers.
    """

    # noinspection PyMethodMayBeStatic
    def precedence(self) -> int:
        return 0

    @abstractmethod
    def apply(self, obj: T) -> T:
        pass


class TransformerGenerator(ABC, Generic[T]):
    # pylint: disable=too-few-public-methods
    """
    Abstract class. Matches a data structure and generates a number of transformers.
    """

    @abstractmethod
    def match(self, obj: T) -> Generator[Transformer[T], None, None]:
        pass


class TransformerSystem(Generic[T]):
    # pylint: disable=too-few-public-methods
    """
    Matches transformer-generators repeatedly and
    applies the highest precedence transformer until none are generated.
    """

    def __init__(self, generators: Iterable[TransformerGenerator[T]]):
        self._generators = generators

    def _iter_matches(self, obj: T):
        for generator in self._generators:
            yield from generator.match(obj)

    def apply(self, obj: T):
        while True:
            transformers = list(self._iter_matches(obj))
            if len(transformers) == 0:
                break
            best = max(transformers, key=lambda x: x.precedence())
            obj = best.apply(obj)
        return obj
