from abc import ABC, abstractmethod
from collections import defaultdict

"""
State Pattern

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


class Item:

    def __init__(self, name, price):
        self.name = name
        self.price = price


class VendingMachineState(ABC):

    @abstractmethod
    def collect_cash(self, vending_machine, cash, item_id):
        pass

    @abstractmethod
    def dispense_item(self, vending_machine, item_id):
        pass

    @abstractmethod
    def cancel_transaction(self, vending_machine, item_id):
        pass


class Ready(VendingMachineState):

    def collect_cash(self, vending_machine, cash, item_id):
        item = vending_machine.get_item(item_id)

        if item is None:
            print('Given item {} is not available in inventory'.format(item_id))

        elif item.price == cash:
            print('The cash given {}$ matches item {} price {}$. Proceeding further'.format(
                cash,
                item.name,
                item.price,
            ))
            vending_machine.add_cash(cash)
            vending_machine.set_state(DispenseItem())
        else:
            raise ValueError(
                'Cash provided for item {item} is {cash} but expected cash '
                'is {expected_cash}'.format(
                    item=item_id,
                    cash=cash,
                    expected_cash=item.price
                ))

    def dispense_item(self, vending_machine, item_id):
        raise NotImplementedError('Cannot dispense item before receiving cash')

    def cancel_transaction(self, vending_machine, item_id):
        raise NotImplementedError('Cannot cancel transaction before receiving cash')


class DispenseItem(VendingMachineState):

    def collect_cash(self, vending_machine, cash, item_id):
        raise NotImplementedError('Cannot receive cash during ongoing transaction')

    def cancel_transaction(self, vending_machine, item_id):
        item = vending_machine.get_item(item_id)
        vending_machine.remove_cash(item.price)
        vending_machine.set_state(Ready())

    def dispense_item(self, vending_machine, item_id):
        item = vending_machine.get_item(item_id)
        if item:
            print('Item {} with id {} is available. Giving it to customer'.format(
                item.name,
                item_id,
            ))
            vending_machine.remove_item(item_id)


class VendingMachine:

    def __init__(self, state=None):
        self.collected_cash = 0
        self.state = state if state else Ready()
        self.items = {}

    def add_cash(self, cash):
        self.collected_cash += cash

    def remove_cash(self, cash):
        self.collected_cash -= cash

    def add_item(self, item_id, name, price):
        self.items[item_id] = Item(name, price)

    def remove_item(self, item_id):
        self.items.pop(item_id)

    def get_item(self, item_id):
        return self.items.get(item_id)

    def dispense_item(self, item_id):
        self.state.dispense_item(self, item_id)

    def collect_cash(self, cash, item_id):
        self.state.collect_cash(self, cash, item_id)

    def cancel_transaction(self, item_id):
        self.state.cancel_transaction(self, item_id)

    def set_state(self, state):
        self.state = state


if __name__ == '__main__':
    vending_machine = VendingMachine()
    vending_machine.add_item(1, 'Chips', 20)
    vending_machine.add_item(2, 'Chocolate', 30)
    item_id = 1
    vending_machine.collect_cash(20, item_id)
    vending_machine.dispense_item(item_id)

"""
Output

Data table_1 is created in table hello. You can do something here
Data table_1 is created in table bye. You can do something here
Alert: Data table_1 was deleted from table bye
"""