##Database Connector##

from pymongo import MongoClient
from redis import Redis
from cassandra.cluster import Cluster


class DBConnector(object):
    def __init__(
        self,
        hostname=None,
        port=None,
        authdb=None,
        username=None,
        password=None
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.authdb = authdb

    def _check_attributes(self, exclude_list=list()):
        attrib_list = ['hostname', 'port', 'authdb', 'username', 'password']
        for attrib in attrib_list:
            if getattr(self, attrib) is None and attrib not in exclude_list:
                answer = raw_input('Please provide me a {}: '.format(attrib))
                if attrib is not 'port':
                    setattr(self, attrib, answer)
                    print getattr(self, attrib)
                else:
                    setattr(self, attrib, int(answer))
                    print getattr(self, attrib)

    def cassandra_connection(self):
        self._check_attributes(['authdb', 'username', 'password'])
        connection = Cluster([self.hostname], port=self.port).connect()
        return connection

    def mongo_connection(self):
        self._check_attributes()
        connection = MongoClient(self.hostname, self.port)
        connection[self.authdb].authenticate(self.username, self.password)
        db = connection['users']
        return db

    def redis_connection(self):
        self._check_attributes(['authdb', 'username'])
        connection = Redis(
            host=self.hostname,
            port=self.port,
            db=self.authdb,
            password=self.password
        )
        return connection
