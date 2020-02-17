from abc import ABC, abstractmethod

"""
- Proxy Pattern is a structural pattern in which proxy object control access to the original object,
allowing to perform something either before or after request is passed to original object
- Example Nginx is a reverse proxy for HTTP request before delegating it to Application server
- Helps in lazy evaluation. You can add the logic in the same class but its better if you create
a proxy for it. In this way, you can have multiple proxies for the same class.
- Can help in logging requests, execution of remote service, providing control access depending on
the type of user, caching requests results and Smart reference.
"""


"""
How to create

1) Create an interface to make service and proxy class interchangeable. If service class is already
implemented, you can also create a proxy subclass of service class
2) Create the proxy class. It should have reference to the service class.
3) Implement the proxy method according to their purposes. In most cases, proxy should delegate the
work to service class
4) (optional) You can have a creation method, that decide whether to use service class or one of the
proxy class.
"""

# Example 1
# Below example does multiple things
# 1) Laze evaluation for loading image
# 2) Caching the image
# 3) Check for permission before getting the image


class ImageViewer(ABC):

    @abstractmethod
    def view_image(self):
        pass


class HighResImageViewer(ImageViewer):

    def __init__(self, file_name):
        self.file_name = file_name
        self.load_image(file_name)

    def load_image(self, file_name):
        print('Loading image {} from a remote machine'.format(file_name))

    def view_image(self):
        print('Showing High Resolution image')


class HighResImageViewerProxy(ImageViewer):

    def __init__(self, file_name):
        self.file_name = file_name
        self.images = {}

    def has_permission(self):
        return self.file_name.split('.')[-1] in self.get_allowed_format()

    @staticmethod
    def get_allowed_format():
        return [
            'jpg',
            'jpeg',
            'png',
        ]

    def view_image(self):
        if self.has_permission() is True:
            if self.images.get(self.file_name) is None:
                self.images[self.file_name] = HighResImageViewer(self.file_name)
            else:
                print('Image already downloaded. No need to download again')
            return self.images[self.file_name].view_image()

        raise Exception('You dont have permission to view the file {}'.format(self.file_name))


if __name__ == '__main__':
    file_name = 'hello_image.jpg'
    image = HighResImageViewerProxy(file_name)
    image.view_image()
    image.view_image()


"""
Output
Loading image hello_image.jpg from a remote machine
Showing High Resolution image
Image already downloaded. No need to download again
Showing High Resolution image
"""