from database import ConnectionPool
from person import Person


class System:
    def __init__(self):
        # create database connection pool
        config = ConnectionPool.get_database_config()
        database_host = config['host']
        database_port = int(config['port'])
        database_user = config['user']
        database_password = config['password']
        database_database = config['database_name']

        self.connection_pool = ConnectionPool(host=database_host,
                                              port=database_port,
                                              user=database_user,
                                              password=database_password,
                                              database_name=database_database)
        self.person = None

    def get_database_connection(self):
        return self.connection_pool.get_connection()

    def release_database_connection(self):
        self.connection_pool.release_connection()

    def set_person_info(self, person_info):
        self.person = person_info


system = System()
