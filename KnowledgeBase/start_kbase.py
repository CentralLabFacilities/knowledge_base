#!/usr/bin/env python

# ros imports
import rospy
from knowledge_base_msgs.srv import *

# config
import yaml
import sys

# handlers
import handling.query_handling as qh
import handling.data_handling as dh

# pymongo and mongoengine
import pymongo
import mongoengine as me

# utils
import utils
import os

# class imports for start_empty
from Classes.KBase import Kbase
from Classes.Arena import Arena
from Classes.RCObjects import Rcobjects
from Classes.Crowd import Crowd


# initialize database node by loading config file
argv = sys.argv
if len(argv) < 2:
    print('Need path to configfile as first parameter!')
    exit('1')
path_to_config = argv[1]
data = yaml.safe_load(open(path_to_config))

# initialize config parameters
db_to_use_as_blueprint_name = data['db_name']
copy_on_startup = data['copy_on_startup']
mongodb_port = int(data['mongodb_port'])
create_on_missing = None
if 'create_on_missing' in data:
    create_on_missing = data['create_on_missing']

print('Config is as follows: ' + str(data))


# check if database files exist
exists = os.path.isfile('/path/to/file')
client = pymongo.MongoClient('localhost', mongodb_port)
dbnames = client.list_database_names()
database_already_exists = db_to_use_as_blueprint_name in dbnames
del client

# check for sanity of database existence
if not create_on_missing and not database_already_exists:
    print('You want to load a database that does not exist! Aborting! (Name of the db: %s)' % db_to_use_as_blueprint_name)
    exit(1)


print('Trying to connect to mongod...')
db_run = None


def reload_database():
    db_run.drop_database('temp_db')
    # copy the blueprint db to the temporary database
    client = pymongo.MongoClient('localhost', mongodb_port)
    client.admin.command('copydb',
                              fromdb=db_to_use_as_blueprint_name,
                              todb='temp_db')


if copy_on_startup and database_already_exists:
    # drop the database from the previous run
    db_run = me.connect('temp_db', host="127.0.0.1", port=mongodb_port)
    reload_database()
else:
    db_run = me.connect(db_to_use_as_blueprint_name, host="127.0.0.1", port=mongodb_port)


if create_on_missing and not database_already_exists:
    print('Creating new, empty Kbase!')
    arena = Arena(rooms=[], doors=[], locations=[])
    crowd = Crowd(persons=[])
    rcobjects = Rcobjects(rcobjects=[])

    kbase = Kbase(arena=arena, crowd=crowd, rcobjects=rcobjects, identifier='TestKBase')
    utils.save_complete_db(kbase)

print('Connected!')


def handle_query(req):
    accepted_w_word = {
        'who': qh.handle_who,
        'what': qh.handle_what,
        'where': qh.handle_where,
        'which': qh.handle_which,
        'in which': qh.handle_in_which,
        'how many': qh.handle_how_many,
        'get': qh.handle_get,

        # unsupported at this point
        'when': qh.handle_when,
        'show': qh.handle_show
    }
    ans = QueryResponse()
    msg = req.query.lower()
    print('DEBUG: got query ' + str(msg))
    query = utils.reduce_query(msg, accepted_w_word)
    print('DEBUG: reduced query ' + str(query))
    q_word = query[0]
    if q_word in accepted_w_word:
        processed_query = accepted_w_word[q_word](query[1:])
        ans.answer = processed_query[0] or 'Failed, unknown error!'
        ans.error_code = processed_query[1]
        ans.success = not ans.error_code
    else:
        ans.answer = 'Failed, bad question word for query: ' + msg
        ans.success = False
        ans.error_code = 0
    print('Success: ' + str(ans.success) + ' Errorcode: ' + str(ans.error_code))
    utils.debug_print(ans.answer)
    return ans


def handle_data(req):
    accepted_d_word = {
        'remember': dh.handle_remember,
        'forget': dh.handle_forget
    }
    ans = DataResponse()
    cmd = req.command.lower()

    print('DEBUG: got command: ' + str(cmd))
    cmd = utils.reduce_query(cmd, accepted_d_word)
    print('DEBUG: reduced query ' + str(cmd))
    d_word = cmd[0]
    if d_word in accepted_d_word:
        ans.success, ans.error_code = accepted_d_word[d_word](cmd[1:])
    else:
        ans.success = False
        ans.error_code = 0
    print('Success: ' + str(ans.success) + ' Errorcode: ' + str(ans.error_code))
    return ans


def handle_reload(req):
    ans = ReloadResponse()

    reload_database()
    print('Reloaded KBase')

    ans.success = copy_on_startup
    return ans


# initialize the rosnode and services
rospy.init_node('knowledge_base')
query_handler = rospy.Service('KBase/query', Query, handle_query)
data_handler = rospy.Service('KBase/data', Data, handle_data)
reload_handler = rospy.Service('KBase/reload', Reload, handle_reload)

print('KBase ready!')
rospy.spin()
