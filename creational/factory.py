from abc import ABC, abstractmethod

"""
Factory Pattern

- Provides an interface for creating objects
- The caller doesn't need to worry about how the object is being created.
- The caller doesn't need to worry about any dependencies needed to create object
- Enforces Open/Closed Principle 
- If you are using mysql and now you want to use postgres or you want to add support for 
  new database you can do it easily
"""

# Example 1


class Language(ABC):

    @abstractmethod
    def say_hello(self):
        pass


class English(ABC):
    def say_hello(self):
        print('Hello')


class French(ABC):

    def say_hello(self):
        print('Bon Jour')


def get_language(language):
    language_mapping = {
        'english': English(),
        'french': French(),
    }
    return language_mapping.get(language.lower())


# Example 2

class DatabaseClient(ABC):

    def __init__(self, connector):
        assert isinstance(connector, Database),\
            'Connector should be subclass of {}'.format(Database.__name__)
        self.connector = connector

    def setupConnection(self):
        print('Creating database connection')
        self.connector.connect()

    def create_table(self, table_name, **kwargs):
        print('Creating table')
        self.connector.create_table(table_name, **kwargs)

    def insert_record(self, record_data):
        print('Inserting record in table')
        self.connector.insert_record(record_data)


class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_table(self, table_name, **kwargs):
        pass

    @abstractmethod
    def insert_record(self, record_data):
        pass


class MysqlDB(Database):

    def connect(self):
        print('creating mysql connection')

    def create_table(self, table_name, **kwargs):
        print('creating table in mysql')

    def insert_record(self, record_data):
        print('insert record in mysql')


class Postgres(Database):

    def connect(self):
        print('creating postgres connection')

    def create_table(self, table_name, **kwargs):
        print('creating table {} in mysql'.format(table_name))

    def insert_record(self, record_data):
        print('insert record in mysql - {}'.format(record_data))


if __name__ == '__main__':
    languages = ['English', 'French']
    for l in languages:
        get_language(l).say_hello()

    db = [Postgres, MysqlDB]

    for database in db:
        db_client = DatabaseClient(database())
        db_client.setupConnection()
        db_client.create_table('test')
        db_client.insert_record('test_record')


"""
Output

Hello
Bon Jour
Creating database connection
creating postgres connection
Creating table
creating table test in mysql
Inserting record in table
insert record in mysql - test_record
Creating database connection
creating mysql connection
Creating table
creating table in mysql
Inserting record in table
insert record in mysql
"""