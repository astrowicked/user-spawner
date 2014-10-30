##Database Connector##

from pymongo import MongoClient
from redis import Redis

class DBConnector(object):
    def __init__(self, hostname=None, port=None, authdb=None, username=None, password=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.authdb = authdb

    def _check_attributes(self, exclude_list=list()):
        for attrib in ['hostname','port','authdb','username','password']:
            if getattr(self,attrib) is None and attrib not in exclude_list:
                if attrib is not 'port':
                    setattr(self,attrib,raw_input('Please provide me a {}: '.format(attrib)))
                    print getattr(self,attrib)
                else:
                    setattr(self,attrib,int(raw_input('Please provide me a {}: '.format(attrib))))
                    print getattr(self,attrib)



    def mongo_connection(self):
        self._check_attributes()
        connection = MongoClient(self.hostname, self.port)
        connection[self.authdb].authenticate(self.username,self.password)
        db = connection['users']
        return db
        
    def redis_connection(self):
        self._check_attributes(['authdb','username'])
        connection = Redis(host=self.hostname,port=self.port,db=self.authdb,password=self.password)
        return connection