from abc import ABC, abstractmethod

import requests

"""
Chain of Responsibility

- Provides a series of handler to process input. You can either return from first successful handler
or pass it to next handler to further process the input.
- The caller doesn't need to worry about any other additional handler if previous handle fails to process input.
- Example - If you need to get IP Address and you have multiple API's to get a host ip. Then if first API fail
to fetch IP, you can use second API and try again and so on (Note: You can also use multithreading for this scenario)
"""

# Example 1


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass


class SimpleCommand(Command):

    def __init__(self, data):
        self.data = data

    def execute(self):
        print("printing data received - {}".format(self.data))


class ComplexCommand(Command):

    def __init__(self, handler):
        self.handler = handler

    def execute(self):
        self.handler.pre_execute()
        self.handler.post_execute()


class ComplexCommandHandler:

    def pre_execute(self):
        print('Pre executing complex handler')

    def post_execute(self):
        print('Post executing complex handler')


class Invoker:

    _on_start = None
    _on_finish = None

    def set_on_start(self, command):
        assert isinstance(command, Command)
        self._on_start = command

    def set_on_finish(self, command):
        assert isinstance(command, Command)
        self._on_finish = command

    def invoke(self):
        if self._on_start:
            print('Invoking on start')
            self._on_start.execute()

        print('Executing invoke method')

        if self._on_finish:
            print('Invoking on end')
            self._on_finish.execute()


if __name__ == '__main__':
    invoker = Invoker()
    invoker.set_on_start(SimpleCommand('hello'))
    handler = ComplexCommandHandler()
    invoker.set_on_finish(ComplexCommand(handler))
    invoker.invoke()


"""
Output

Invoking on start
printing data received - hello
Executing invoke method
Invoking on end
Pre executing complex handler
Post executing complex handler
"""