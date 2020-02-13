from abc import ABC, abstractmethod

"""
State Pattern

- State is a behavioral design pattern that lets an object alter its behavior when its internal
state changes
- Very useful for programs having finite state machine.
- Follow Open Close Relationship and Single Responsibility principle
- Example - Vending Machine. A vending machine can be in "Ready", "Dispensing Item", "Dispensing Change"
"Transaction Rollback" state. Each state will determine what actions it can perform. So instead of using single
class and using switch/if-else and cluttering everything in one place, we can use state pattern for state
management.
"""


"""
How to create

1) Create a Manager that will delegate all its work to a state class. This expose setter to change
state
2) Create a interface/base class that all state class will inherit
3) Create different state class. You can also pass the manager object so that they get additional
info from manager class
4) The state class will do something and may be set new state. For this, it must have access to
Manager class object. Or you can use client code or Manager class to change the state. To avoid
any possibilities of setting new state, use only manager/state class to change to next state.  
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
        print('Transaction for item - {} is successfully cancelled'.format(item_id))
        vending_machine.set_state(Ready())

    def dispense_item(self, vending_machine, item_id):
        item = vending_machine.get_item(item_id)
        if item:
            print('Item {} with id {} is available. Giving it to customer'.format(
                item.name,
                item_id,
            ))
            vending_machine.remove_item(item_id)
        else:
            print('The transaction is cancelled. Please order again')


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
    vending_machine.cancel_transaction(item_id)
    vending_machine.dispense_item(item_id)

    vending_machine.collect_cash(20, item_id)
    vending_machine.dispense_item(item_id)

"""
Output

The cash given 20$ matches item Chips price 20$. Proceeding further
Transaction for item - 1 is successfully cancelled
NotImplementedError: Cannot dispense item before receiving cash


The cash given 20$ matches item Chips price 20$. Proceeding further
Item Chips with id 1 is available. Giving it to customer

"""