from collections.abc import Iterable, Iterator
from typing import List, Any

"""
Command Pattern

- Provides a command based interface to execute instead of message oriented interface
- Can Provide undo operations.
- Encapsulates all information needed to perform an action or trigger an event
- Example - Move Command providing move and undo operations.
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


if __name__ == '__main__':
    collection = WordsCollection([])
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    print("Straight traversal:")
    print("\n".join(collection))
    print("")

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()), end="")

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