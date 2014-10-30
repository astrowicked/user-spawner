import config
from datetime import datetime
import doc_generator
from db_connector import DBConnector
import hashlib

dg = doc_generator.DocumentGenerator()

def write_to_redis(num_to_generate=0):
    db = DBConnector(config.REDIS_HOST,config.REDIS_PORT, config.REDIS_PASSWORD).redis_connection()
    num = 0
    if num_to_generate == 0:
        num_to_generate = int(raw_input("Please provide a number of users you would like to spawn: "))
    start = datetime.now()
    print "Starting to insert {} docs at {}.".format(num_to_generate,start)
    for num in xrange(num_to_generate):
        doc = dg.generate_user_doc()
        print doc
        print doc['last_name']
        print doc['first_name']
        print doc['age']
        print doc['date_joined']
        to_hash = "{}{}{}{}".format(doc['last_name'],
        doc['first_name'],doc['age'],doc['date_joined'])
        print to_hash
        doc_hash = hashlib.sha256(to_hash).hexdigest()
        print doc_hash
        db.hmset(doc_hash, doc)
        db.lpush('doc_list', doc_hash)
        num += 1
        end = datetime.now()
        print "Finished inserting {} docs at {}.".format(num,end)
        print "Took {} to complete.".format(end-start)
    return db.hgetall('users')

def write_to_mongo(num_to_generate=0):
    db = DBConnector(config.MONGO_HOST,config.MONGO_PORT,config.MONGO_AUTHDB, config.MONGO_USER, config.MONGO_PASSWORD).mongo_connection()
    num = 0
    user_list = []
    if num_to_generate == 0:
        num_to_generate = int(raw_input("Please provide a number of users you would like to spawn: "))
    start = datetime.now()
    print "Starting to generate {} docs at {}.".format(num_to_generate,start)
    for num in xrange(num_to_generate):
      user_list.append(dg.generate_user_doc())
      #db.users.insert(generate_user_doc())
      num += 1
    end = datetime.now()
    print "Finished generating {} docs at {}.".format(num,end)
    print "Took {} to complete.".format(end-start)
    print "\nStarting to insert {} docs at {}.".format(num_to_generate,start)
    db.users.insert(user_list)
    end = datetime.now()
    print "Finished inserting {} docs at {}.".format(num,end)
    print "Took {} to complete.".format(end-start)

db_tech = raw_input("Where would you like to store the users? [Mongo or Redis] ")
if db_tech == 'Mongo' or db_tech == 'mongo':
    write_to_mongo()
elif db_tech == 'Redis' or db_tech == 'redis':
    write_to_redis()
else:
    print "You didn't choose a valid DB technology."