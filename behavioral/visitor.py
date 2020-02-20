from abc import ABC, abstractmethod

"""
Visitor Pattern

- Visitor design pattern is a way of separating an algorithm from an object structure on 
which it operates.
- To enhance  the functionality of class, you can update the existing class. But you can introduce
some bugs on existing functionality or you may add so many functionality to the class that now its
hard to maintain. Another option is to to create a subclass and add the specific functionality. But
this can result in to many subclasses and it will be very hard to keep track and maintain all of it.
- To solve above issue, we can create a visitor class that will take the specific class as parameter
and implement its functionality. The Visitor will implement different methods for a series of
related class. These methods may have different signature and return type depending upon the type
of class for which we are implementing the method. The visitor takes the instance reference as input
and implements the goal through double dispatch. There are two ways to call visitor class

1) Implement accept method in each classes that need additional functionality. This will inturn call
visitor's concrete implementation
2) Use introspection in the visitor class. This will result in no modification in existing class

- Use the Visitor to clean up the business logic of auxiliary behaviors
- Example - You have different expression (literal, addition etc), and you want to provide pretty
print functionality.
"""


"""
How to create

1) Create Visitor class that will implement method for one or more main classes.
2) Creat
3) Create different Algorithm class.
4) Add a field for storing reference of algorithm in context class and also provide setter to change
the algorithm.
5) Client can then choose the algorithm as per the different criteria. 
"""

# Example 1
# Below example create a ExpressionVisitor class for pretty printing. Instead of adding logic to the
# the expresssion class, we implemented it on visitor class. The visitor class use introspection
# and call the appropriate method.


class ExpressionVisitor:

    def __init__(self):
        self.result = ""

    def visit(self, expression, *args, **kwargs):
        method = None
        for cls in expression.__class__.__mro__:
            method_name = 'pretty_print_{}'.format(cls.__name__.lower())
            method = getattr(self, method_name, None)
            if method:
                break

        if not method:
            raise NotImplementedError(
                'Please implement pretty print implementation for class {}'.format(
                    expression.__class__.__name__,
                )
            )

        return method(expression, *args, **kwargs)

    def pretty_print_addition(self, addition, *args, **kwargs):
        self.result += "("
        self.visit(addition.left)
        self.result += "+"
        self.visit(addition.right)
        self.result += ")"

    def pretty_print_literal(self, literal, *args, **kwargs):
        self.result += str(literal.value)


class Literal:

    def __init__(self, value):
        self.value = value


class Addition:

    error_msg = 'Literal should be an instance of {}'.format(Literal.__class__.__name__)

    def __init__(self, left, right):
        self.left = left
        self.right = right


if __name__ == '__main__':
    expression = Addition(Literal(1), Addition(Literal(2), Literal(6)))
    visitor = ExpressionVisitor()
    visitor.visit(expression)
    print(visitor.result)


"""
Output
(1+(2+6))
"""