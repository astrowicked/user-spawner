user-spawner v0.1
============

This is a mock user profile genetator that will store generated user profiles into a database.

Config
-------

Fill out the config.py with your connection details:

```
    ##MONGO##
    MONGO_HOST = None
    MONGO_PORT = None
    MONGO_USER = None
    MONGO_PASSWORD = None
    MONGO_AUTHDB = None

    ##REDIS##
    REDIS_HOST = None
    REDIS_PORT = None
    REDIS_PASSWORD = None
    REDIS_DB = None
```


Usage
------

Run the user_spawner.py:

`python user_spawner.py`

If you do not have any details in your config, you will get prompted for input:

```
python user_spawner.py
Please provide me a hostname:
```

It will run through parameters that you have not set in the config.

Once you have all the entered you will get prompted for number of users to spawn:

```
Please provide a number of users you would like to spawn:
```

It will also give you some stats around the generation and insert times:

```
Starting to generate 1000 docs at 2014-10-30 17:12:38.179934.
Finished generating 1000 docs at 2014-10-30 17:12:38.195511.
Took 0:00:00.015577 to complete.

Starting to insert 1000 docs at 2014-10-30 17:12:38.179934.
Finished inserting 1000 docs at 2014-10-30 17:12:38.399998.
Took 0:00:00.220064 to complete.
```

Requirements
-------------

pymongo
redis

These can be installed using PIP and the requirements.txt file in the root of the repo:

`pip install -r requirements.txt`

Upcoming
-------------
 - Option to specify whether using authentication or not
 - Support for storing in Cassandra
 - Profile types (Ex. Fitness app, Social Media app, Gaming app, etc..)
 - Convert for full CLI use with options and help
