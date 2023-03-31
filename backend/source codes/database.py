import configparser
import os

import pymysql.cursors


class ConnectionPool:
    def __init__(self, host, port, user, password, database_name, max_connections=10):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name
        self.max_connections = max_connections
        self.connections = []

    def create_connection(self):
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def get_connection(self):
        """
        获取一个数据库连接。
        如果连接池中没有可用连接，则创建一个新连接并返回。
        """
        if len(self.connections) == 0:
            return self.create_connection()
        else:
            return self.connections.pop()

    def release_connection(self, connection):
        """
        释放一个数据库连接，并将其加入连接池中。
        如果连接池中连接的数量已经达到最大值，则直接释放该连接。
        """
        if len(self.connections) >= self.max_connections:
            connection.close()
        else:
            self.connections.append(connection)

    @staticmethod
    def get_database_config():
        if os.path.exists('backend/source codes/config.ini'):
            # 读取配置文件中的数据库连接信息
            config_file = configparser.ConfigParser()
            config_file.read('backend/source codes/config.ini')

            config_database_host = config_file.get('database', 'host')
            config_database_port = config_file.get('database', 'port')
            config_database_user = config_file.get('database', 'user')
            config_database_password = config_file.get('database', 'password')
            config_database_database = config_file.get('database', 'database')

            return {
                'host': config_database_host,
                'port': config_database_port,
                'user': config_database_user,
                'password': config_database_password,
                'database_name': config_database_database
            }
        else:
            raise FileNotFoundError('config.ini not found')
            return None


config = ConnectionPool.get_database_config()
database_host = config['host']
database_port = int(config['port'])
database_user = config['user']
database_password = config['password']
database_database = config['database_name']

CONNECTION_POOL = ConnectionPool(host=database_host, port=database_port, user=database_user, password=database_password,
                                 database_name=database_database)
