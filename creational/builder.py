from abc import ABC, abstractmethod

"""
Builder Pattern

- Builder design pattern is a way of creating of complex objects by providing a flexible solutions
to create it.
- You can create different representation of the same object or object with different configurations
- It also eliminate need to create a complex constructor and inheritence.
- In Python, construction of object is very flexible(args and kwargs) so you dont need any fancy 
code to implement this
"""


"""
How to create (For language without support of named arguments in constructor)

1) Create common construction interface for building products.
2) Create concrete builder class for each product representations
3) (Optional) Create a director class to provide common products.
4) Create builder and/or director in client code. The object can be retrived from builder/director
"""

# Example 1


class Building:

    def __init__(self):
        self.floor = self.build_floor()
        self.size = self.build_size()

    def build_floor(self):
        raise NotImplementedError

    def build_size(self):
        raise NotImplementedError

    def __repr__(self):
        return 'Floor: {0.floor} | Size: {0.size}'.format(self)


# Concrete Buildings
class House(Building):
    def build_floor(self):
        return 'One'

    def build_size(self):
        return 'Big'


class Flat(Building):
    def build_floor(self):
        return 'More than One'

    def build_size(self):
        return 'Small'


if __name__ == '__main__':
    h = House()
    print(h)
    f = Flat()
    print(f)


"""
Output
Floor: One | Size: Big
Floor: More than One | Size: Small
"""