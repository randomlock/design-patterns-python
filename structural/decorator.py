from abc import ABC, abstractmethod

"""
- Decorator Pattern is a structural pattern in which is used to dynamically add a new feature to an
object without changing its implementation
- Example You have have class that display paragraph. Now you want to make it bold or italic or
bold italic. Instead of altering the existing class, you can create decorator class that implement
similar method and do its thing and call other decorator method
- Decorator is also called "Smart Proxy." This is used when you want to add functionality to an 
object, but not by extending that object's type. This allows you to do so at runtime.
- Decorator and Proxy have similar structures, but very different intents. Both patterns are built 
on the composition principle, where one object is supposed to delegate some of the work to another. 
The difference is that a Proxy usually manages the life cycle of its service object on its own, 
whereas the composition of Decorators is always controlled by the client.
- Example You want to send sms, email and message to slack in any combination i.e you can choose sms
+ email or sms+slack or sms+slack+email. You can create an adapter(inheritence) for all these but
there will be two many adapters.
"""


"""
How to create

1) The component class and decorators class should respect a common interface. This is because of decorators
are optional. We may or may not use one or more decorators to update functionality of component class
2) Create a component class implementing the above interface. The class should provide basic behavior
which decorator class can update/modify.
3) Create a base decorator class implementing the same above interface. It should also have access
to wrapped object(component class) through composition.
4) Define extra behaviour in decorator class before or after calling parent class.
5) Add combinations of decorator in client class as per the needs.
"""

# Example 1


class Text(ABC):

    # It's better if we have common interface for component class and decorator class. So that we
    # can call component class with or without decorator.

    @abstractmethod
    def render(self):
        pass


class TextTag(Text):

    def __init__(self, text):
        self.text = text

    def render(self):
        return '<p>{}</p>'.format(self.text)


class BaseTextWrapper(Text):

    # You can create a base decorator to include common methods. In this example, it doesn't do
    # anything other than calling render method of wrapped object.

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def render(self):
        return self.wrapped.render()


class BoldWrapper(BaseTextWrapper):

    def render(self):
        return '<B>{}</B>'.format(self.wrapped.render())


class ItalicWrapper(BaseTextWrapper):

    def render(self):
        return '<i>{}</i>'.format(self.wrapped.render())


if __name__ == '__main__':
    text = 'hello world'
    simple_text = TextTag(text)
    bold_text = BoldWrapper(simple_text)
    italic_text = ItalicWrapper(simple_text)
    bold_italic_text = BoldWrapper(ItalicWrapper(simple_text))
    italic_bold_text = ItalicWrapper(BoldWrapper(simple_text))
    print(simple_text.render())
    print(bold_text.render())
    print(italic_text.render())
    print(bold_italic_text.render())
    print(italic_bold_text.render())


"""
Output
<p>hello world</p>
<B><p>hello world</p></B>
<i><p>hello world</p></i>
<B><i><p>hello world</p></i></B>
<i><B><p>hello world</p></B></i>
"""