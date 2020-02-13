from abc import ABC, abstractmethod

"""
Strategy Pattern

- Strategy is a behavioral design pattern that lets you change algorithm in runtime as per client
need without changing class that call that algorithm
- Instead of hard coding multiple algorithm in one class and make object behave differently we can
separate algorithm implementation and algorithm caller. The algorithm class should respect a 
common interface
- Follow Open Close Relationship and Single Responsibility principle
- Example - Sorting. Let say you created multiple algorithm to sort item. The efficiency of the 
algorithm is determined by the type and nature of data. So we need to give different algorithm on 
different item. We can use strategy pattern to create different implementation of sorting algorithm 
which will be called by caller as per client need.
"""


"""
How to create

1) In context class identify algorithm which are prone to changes.
2) Create a interface/base class that is common for all variant of the algorithm
3) Create different Algorithm class.
4) Add a field for storing reference of algorithm in context class and also provide setter to change
the algorithm.
5) Client can then choose the algorithm as per the different criteria. 
"""


class SortStrategy(ABC):

    @abstractmethod
    def sort(self, items):
        pass


class MergeSort(SortStrategy):

    def sort(self, items):
        print('Sorting items using merge sort')


class QuickSort(SortStrategy):

    def sort(self, items):
        print('Sorting items using quick sort')


class TimSort(SortStrategy):

    def sort(self, items):
        print('Sorting items using tim sort')


class Sort:

    def __init__(self, strategy=None):
        self.strategy = strategy if strategy else MergeSort()

    def set_sort_strategy(self, strategy):
        self.strategy = strategy

    def sort(self, items):
        self.strategy.sort(items)


if __name__ == '__main__':
    items = [1, 2, 4, 5]

    sort_cls = Sort()
    sort_cls.sort(items)

    sort_cls.set_sort_strategy(TimSort())
    sort_cls.sort(items)


"""
Output
Sorting items using merge sort
Sorting items using tim sort
"""