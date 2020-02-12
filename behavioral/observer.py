import enum
from abc import ABC, abstractmethod
from collections import defaultdict

"""
Observer Pattern

- Provides a mechanism for publish-subscribe model
- Very useful for event based programming where changes in source triggers different targets
- Follow Open Close Relationship
- Example - Database triggers. When you are creating/updating a record and you need to perform some
  actions before/after it
"""


"""
How to create

1) Create a Manager that will handle subscriptions
2) Create a publisher that will notify the manger about state change
3) Create subscribers that implement a common interface. You can pass reference to publisher as 
    different subscriber may need different data
4) In the client code, add relevant subscriber to relevant event type.
"""


class EventType(enum.Enum):
    create = 0
    update = 1
    delete = 2
    retrieve = 4


class SignalManager(ABC):

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, listener):
        assert isinstance(listener, Listener)
        self.subscribers[event_type].append(listener)

    def un_subscribe(self, event_type, listener):
        if listener in self.subscribers[event_type]:
            self.subscribers[event_type].remove(listener)
            return
        raise ValueError('Listener {} is not subscribed to event - {}'.format(listener, event_type))

    def notify(self, publisher, event_type, *args, **kwargs):
        for subscriber in self.subscribers.get(event_type, []):
            subscriber.notify(publisher, *args, **kwargs)


class Signal:

    def __init__(self):
        self.db_record = defaultdict(list)
        self.signal_manager = SignalManager()

    def on_create(self, table, data):
        self.db_record[table].append(data)
        self.signal_manager.notify(self, EventType.create, table, data)

    def on_delete(self, table, data):
        self.db_record[table].remove(data)
        self.signal_manager.notify(self, EventType.delete, table, data)


class Listener(ABC):

    @abstractmethod
    def notify(self, publisher, *args, **kwargs):
        pass


class LoggingListener(Listener):

    def notify(self, publisher, *args, **kwargs):
        print('Data {} is created in table {}. You can do something here'.format(args[0], args[1]))


class EmailAlertListener(Listener):

    def notify(self, publisher, *args, **kwargs):
        print('Alert: Data {} was deleted from table {}'.format(args[0], args[1]))


if __name__ == '__main__':
    signal = Signal()
    logging_listener = LoggingListener()
    email_listener = EmailAlertListener()
    signal.signal_manager.subscribe(EventType.create, logging_listener)
    signal.signal_manager.subscribe(EventType.delete, email_listener)
    signal.on_create(table='table_1', data='hello')
    signal.on_create(table='table_1', data='bye')
    signal.on_delete(table='table_1', data='bye')

"""
Output

Data table_1 is created in table hello. You can do something here
Data table_1 is created in table bye. You can do something here
Alert: Data table_1 was deleted from table bye
"""