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


class BaseHandler(ABC):

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self,):
        result = self.get_ip()
        if result is None and self._next_handler is not None:
            return self._next_handler.handle()
        return result

    @abstractmethod
    def get_ip(self):
        pass


class RetrieveIPFromSourceA(BaseHandler):

    def get_ip(self):
        return requests.get('https://api6.ipify.org?format=json').json().get('ip')


class RetrieveIPFromSourceB(BaseHandler):

    def get_ip(self):
        return requests.get('https://ipapi.co/8.8.8.8/json/').json()


if __name__ == '__main__':
    handler = RetrieveIPFromSourceA()
    handler.set_next(RetrieveIPFromSourceB())
    print(handler.handle())


"""
Output
182.68.28.91
"""