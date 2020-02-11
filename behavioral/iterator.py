from collections.abc import Iterable, Iterator
from typing import Any

"""
Iterator Pattern

- Allow sequential traversal of complex data structure
- Allow you to define generator for iterations.
- Example - Iterator for odd number, even number, catalan number, prime number.
- Example - Iterator to traverse list of dict sorted by a tuple of keys.
"""

# Example 1


class WordsCollection(Iterable):

    def __init__(self, _collection) -> None:
        self._collection = _collection

    def __iter__(self):
        return AlphabeticalIterator(self._collection, reverse=False)

    def get_reverse_iterator(self):
        return AlphabeticalIterator(self._collection, reverse=True)

    def add_item(self, item: Any):
        self._collection.append(item)


class AlphabeticalIterator(Iterator):

    def __init__(self, _collection, reverse=False):
        self._collection = _collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value

# Example 2


def count_to(count):
    """Counts by word numbers, up to a maximum of five"""
    numbers = ["one", "two", "three", "four", "five"]
    for number in numbers[:count]:
        yield number


# Test the generator
count_to_two = lambda: count_to(2)
count_to_five = lambda: count_to(5)


if __name__ == '__main__':
    collection = WordsCollection([])
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    print("Straight traversal:")
    print("\n".join(collection))
    print("")

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()))

    for number in count_to_five():
        print(number)

"""
Output

Straight traversal:
First
Second
Third

Reverse traversal:
Third
Second
First
"""