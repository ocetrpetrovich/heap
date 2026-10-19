from collections.abc import Callable, Iterator, Iterable
from typing import Protocol, Self


class SupportsLessOrEqual(Protocol):
    def __le__(self, other: Self, /) -> bool: ...


class Heap[T]:
    def __init__(
            self,
            items: Iterable[T] = (),
            /,
            *,
            key: Callable[[T], SupportsLessOrEqual] = lambda item: item,
            reverse: bool = False
    ):
        self._storage: list[tuple[SupportsLessOrEqual, int, T]] = []  # [..., (key, id, value), ...]
        self._key: Callable[[T], SupportsLessOrEqual] = key
        self._reverse: bool = reverse
        self._id_counter: int = 0

        for item in items:
            self._storage.append((self._key(item), self._id_counter, item))
            self._id_counter += 1
        for index in range((len(self._storage)) // 2 - 1, -1, -1):
            self._sift_down(index)

    def _parent(self, index: int) -> int:
        return 0 if index == 0 else (index - 1) // 2

    def _left(self, index: int) -> int:
        return left if (left := index * 2 + 1) < len(self._storage) else index

    def _right(self, index: int) -> int:
        return right if (right := index * 2 + 2) < len(self._storage) else index

    def _less_or_equal(self, first: int, second: int, /) -> bool:
        if first == second:
            return True
        return self._reverse != (self._storage[first][:2] <= self._storage[second][:2])

    def _swap(self, first: int, second: int, /):
        self._storage[first], self._storage[second] = self._storage[second], self._storage[first]

    def _sift_up(self, index: int, /):
        while not self._less_or_equal(parent := self._parent(index), index):
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index: int, /):
        while True:
            left = self._left(index)
            right = self._right(index)
            left_f = not self._less_or_equal(index, left)
            right_f = not self._less_or_equal(index, right)
            if not left_f and not right_f:
                break
            if left_f and right_f:
                left_f = self._less_or_equal(left, right)
            if left_f:
                self._swap(index, left)
                index = left
            else:
                self._swap(index, right)
                index = right

    def push(self, item: T, /):
        self._storage.append((self._key(item), self._id_counter, item))
        self._id_counter += 1

        self._sift_up(len(self._storage) - 1)

    def pop(self) -> T:
        if not self._storage:
            raise IndexError("pop from empty Heap")
        self._storage[0], self._storage[-1] = self._storage[-1], self._storage[0]
        _, _, item = self._storage.pop()
        if self._storage:
            self._sift_down(0)
        return item

    def get(self) -> T:
        if not self._storage:
            raise IndexError("get from empty Heap")
        return self._storage[0][2]

    def extend(self, items: Iterable[T], /):
        for item in items:
            self.push(item)

    def clear(self):
        self._storage.clear()

    def __len__(self) -> int:
        return len(self._storage)

    def __bool__(self) -> bool:
        return bool(self._storage)

    def __contains__(self, item: T) -> bool:
        return item in map(lambda s: s[2], self._storage)

    def __iter__(self) -> Iterator[T]:
        return map(lambda s: s[2], self._storage)

    def copy(self) -> Heap[T]:
        copy = Heap[T](key=self._key, reverse=self._reverse)
        copy._storage = self._storage.copy()
        return copy


h1 = Heap([2, 43, 56, 76, 8, 5, 4, 7, 3, 7, 3])

h2 = Heap[int | float | str](key=int)
# в каком порядке элементы добавлялись, в таком и выходят (если говорим про элементы с равными key)
h2.push(0)
h2.push(0.0)
h2.push("0")
# сравниваем именно по ключу
h2.push(1.4)
h2.push(1.3)
h2.push(1.5)
# можем добавлять разное
h2.extend(["123", 1234.1234, 67, "76"])

h3 = Heap(h2, key=int, reverse=True)

while h1:
    print(h1.get(), end=" ")
    h1.pop()
print()

while h2:
    print(repr(h2.pop()), end=" ")
print()

while h3:
    print(repr(h3.pop()), end=" ")
print()
