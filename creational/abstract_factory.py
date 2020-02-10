import os
from abc import ABC, abstractmethod

"""
Abstract Factory Pattern

- Provides an interface for creating related objects without specifying their concrete class
- The caller doesn't need to worry about any comptibility issue
- The caller doesn't need to worry about any dependencies needed to create object
- Enforces Open/Closed and Single Responsibility Principle 
- If you are using Mysql database, then your QuerysetManager should also support mysql.
"""

MYSQL = 'mysql'
POSTGRES = 'postgres'


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


class Mysqldb(Database):

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


class BaseManager(ABC):

    @abstractmethod
    def filter(self, *args, **kwargs):
        pass

    @abstractmethod
    def ordering(self, *args, **kwargs):
        pass


class PostgresManager(BaseManager):

    def filter(self, *args, **kwargs):
        print('applying postgres filtering')

    def ordering(self, *args, **kwargs):
        print('applying postgres ordering')


class MysqlManager(BaseManager):

    def filter(self, *args, **kwargs):
        print('applying mysql filtering')

    def ordering(self, *args, **kwargs):
        print('applying mysql ordering')


class DBClient:

    def __init__(self):
        self.db = self.create_db()
        self.manager = self.create_manager()

    @abstractmethod
    def create_manager(self):
        pass

    @abstractmethod
    def create_db(self):
        pass


class PostgresClient(DBClient):

    def create_manager(self):
        return PostgresManager()

    def create_db(self):
        return Postgres()


class MysqlClient(DBClient):

    def create_manager(self):
        return MysqlManager()

    def create_db(self):
        return Mysqldb()


def get_mysql_client(db_config):
    if db_config == MYSQL:
        return MysqlClient()
    if db_config == POSTGRES:
        return PostgresClient()


if __name__ == '__main__':
    db_config = os.environ.get('DB_CONFIG', MYSQL)
    client = get_mysql_client(db_config)
    print('Manager class is {}'.format(client.manager.__class__.__name__))
    print('Database class is {}'.format(client.db.__class__.__name__))
    client.manager.filter(num__gt=6)
    client.manager.ordering('-id')


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