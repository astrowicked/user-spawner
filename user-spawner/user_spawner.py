import config
from datetime import datetime
import doc_generator
from db_connector import DBConnector
import hashlib
from cassandra import InvalidRequest
import uuid
import sys

dg = doc_generator.DocumentGenerator()


def write_to_redis(num_to_generate=0):
    db = DBConnector(
        config.REDIS_HOST,
        config.REDIS_PORT,
        config.REDIS_PASSWORD
    ).redis_connection()
    num = 0
    if num_to_generate == 0:
        num_to_generate = int(raw_input(
            "Please provide a number of users you would like to spawn: "
        ))
    start = datetime.now()
    pipe = db.pipeline()
    print "Starting to insert {} docs at {}.".format(num_to_generate, start)
    for num in xrange(num_to_generate):
        doc = dg.generate_user_doc()
        to_hash = "{}{}{}{}".format(
            doc['last_name'],
            doc['first_name'],
            doc['age'],
            doc['date_joined']
        )
        doc_hash = hashlib.sha256(to_hash).hexdigest()
        pipe.hmset(doc_hash, doc)
        pipe.lpush('doc_list', doc_hash)
        num += 1
        end = datetime.now()
    values = pipe.execute()
    print values
    print "Finished inserting {} docs at {}.".format(num, end)
    print "Took {} to complete.".format(end-start)
    return db.hgetall('users')


def write_to_mongo(num_to_generate=0):
    db = DBConnector(
        config.MONGO_HOST,
        config.MONGO_PORT,
        config.MONGO_AUTHDB,
        config.MONGO_USER,
        config.MONGO_PASSWORD
    ).mongo_connection()
    num = 0
    user_list = []
    if num_to_generate == 0:
        num_to_generate = int(raw_input(
            "Please provide a number of users you would like to spawn: "
        ))
    start = datetime.now()
    print "Starting to generate {} docs at {}.".format(num_to_generate, start)
    for num in xrange(num_to_generate):
        user_list.append(dg.generate_user_doc())
        #db.users.insert(generate_user_doc())
        num += 1
    end = datetime.now()
    print "Finished generating {} docs at {}.".format(num, end)
    print "Took {} to complete.".format(end-start)
    print "\nStarting to insert {} docs at {}.".format(num_to_generate, start)
    db.users.insert(user_list)
    end = datetime.now()
    print "Finished inserting {} docs at {}.".format(num, end)
    print "Took {} to complete.".format(end-start)


def write_to_cassandra(num_to_generate=0):
    db = DBConnector(
        config.CASSANDRA_HOST,
        config.CASSANDRA_PORT
    ).cassandra_connection()
    try:
        db.set_keyspace('users')
    except InvalidRequest:
        answer = raw_input(
            "The keyspace 'users' doesn't exist, would you like to create it? "
        )
        if answer in ['Y', 'y', 'yes', 'YES', 'Yes']:
            db.execute(
                """
                CREATE KEYSPACE users
                WITH replication
                = {'class':'SimpleStrategy', 'replication_factor':1}
                """
            )
        else:
            print "Big Gulps huh?   Well, See ya later!"
            sys.exit(0)
    num = 0
    if num_to_generate == 0:
        num_to_generate = int(raw_input(
            "Please provide a number of users you would like to spawn: "
        ))
    start = datetime.now()
    print "\nStarting to insert {} docs at {}.".format(num_to_generate, start)
    #print "Starting to generate {} docs at {}.".format(num_to_generate, start)
    for num in xrange(num_to_generate):
        doc = dg.generate_user_doc()
        doc['user_id'] = uuid.uuid4()
        query = """INSERT INTO users (
                    user_id,
                    first_name,
                    last_name,
                    age,
                    date_joined
                    )
                   VALUES (
                    %(user_id)s,
                    %(first_name)s,
                    %(last_name)s,
                    %(age)s,
                    %(date_joined)s
                    )
                """
        try:
            db.execute(query, doc)
        except InvalidRequest:
            answer = raw_input(
                "The table 'users' doesn't exist, would you like it created? "
            )
            if answer in ['Y', 'y', 'yes', 'YES', 'Yes']:
                db.execute(
                    """
                    CREATE TABLE users (
                        user_id uuid,
                        first_name text,
                        last_name text,
                        age int,
                        date_joined timestamp,
                        PRIMARY KEY (user_id)
                        )
                    """
                )
            db.execute(query, doc)
        num += 1
    end = datetime.now()
    #print "Finished generating {} docs at {}.".format(num, end)
    #print "Took {} to complete.".format(end-start)
    #print "\nStarting to insert {} docs at {}.".format(num_to_generate, start)
    end = datetime.now()
    print "Finished inserting {} docs at {}.".format(num, end)
    print "Took {} to complete.".format(end-start)

db_tech = raw_input(
    "Where would you like to store the users? [Cassandra, Mongo or Redis] "
)
if db_tech == 'Mongo' or db_tech == 'mongo':
    write_to_mongo()
elif db_tech == 'Redis' or db_tech == 'redis':
    write_to_redis()
elif db_tech == 'Cassandra' or db_tech == 'cassandra':
    write_to_cassandra()
else:
    print "You didn't choose a valid DB technology."
