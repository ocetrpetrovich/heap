from collections.abc import Callable, Iterator, Iterable
from typing import Protocol, Self


class SupportsLessOrEqual(Protocol):
    def __le__(self, other: Self, /) -> bool: ...


class Heap[T]:
    def __init__(self, items: Iterable[T] = (), *, key: Callable[[T], SupportsLessOrEqual] = lambda item: item, reverse: bool = False):
        self._storage: list[tuple[SupportsLessOrEqual, int, T]] = []  # [..., (key, count, value), ...]
        self._key: Callable[[T], SupportsLessOrEqual] = key
        self._reverse: bool = reverse
        self._counter: int = 0

        for item in items:
            self._storage.append((self._key(item), self._counter, item))
            self._counter += 1
        for i in range(len(self._storage) - 1, 0, -1):
            self._sift_down(i)

    def _heap_rule(self, index: int) -> bool:
        return index == 0 or self._reverse != (self._storage[index][:2] <= self._storage[(index - 1) // 2][:2])

    def _swap(self, index: int):
        self._storage[index], self._storage[(index - 1) // 2] = (
            self._storage[(index - 1) // 2], self._storage[index]
        )

    def _sift_up(self, index: int):
        while not self._heap_rule(index):
            self._swap(index)
            index = (index - 1) // 2

    def _sift_down(self, index: int):
        while not ((left := self._heap_rule(index * 2 + 1)) and self._heap_rule(index * 2 + 2)):
            index = index * 2 + (2 if left else 1)
            self._swap(index)

    def push(self, item: T):
        self._storage.append((self._key(item), self._counter, item))
        self._counter += 1

        self._sift_up(len(self._storage) - 1)

    def pop(self) -> T:
        if not self._storage:
            raise IndexError("pop from empty Heap")
        self._storage[0], self._storage[-1] = self._storage[-1], self._storage[0]
        _, _, item = self._storage.pop(0)
        self._sift_down(0)
        return item

    def get(self) -> T:
        if not self._storage:
            raise IndexError("get from empty Heap")
        return self._storage[0][2]

    def extend(self, items: Iterable[T]):
        for item in items:
            self.push(item)

    def clear(self):
        self._storage.clear()

    def __len__(self) -> int:
        return len(self._storage)

    def __bool__(self) -> bool:
        return bool(self._storage)

    def __contains__(self, item: T) -> bool:
        return item in map(lambda s: s[3], self._storage)

    def __iter__(self) -> Iterator[T]:
        return map(lambda s: s[3], self._storage)
