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

#utils
import utils


# initialize database node by loading config file
argv = sys.argv
if len(argv) < 2:
    print('Need path to configfile as first parameter!')
    exit('1')
path_to_config = argv[1]
data = yaml.safe_load(open(path_to_config))

#initialize config parameters
db_to_use_as_blueprint_name = data['db_name']
copy_on_startup = data['copy_on_startup']
mongodb_port = int(data['mongodb_port'])

print('Trying to connect to mongod...')

if copy_on_startup:
    # drop the database from the previous run
    db_run = me.connect('temp_db', host="127.0.0.1", port=mongodb_port)
    db_run.drop_database('temp_db')
    # copy the blueprint db to the temporary database
    client = pymongo.MongoClient('localhost', mongodb_port)
    client.admin.command('copydb',
                              fromdb=db_to_use_as_blueprint_name,
                              todb='temp_db')

else:
    me.connect(db_to_use_as_blueprint_name)

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
    msg = repr(req.query)[1:-1].lower()
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
    return ans



def handle_data(req):
    accepted_d_word = {
        'remember': dh.handle_remember,
        'forget': dh.handle_forget
    }
    ans = DataResponse()
    cmd = repr(req.command)[1:-1].lower()

    print('DEBUG: got command: ' + str(cmd))
    cmd = utils.reduce_query(cmd, accepted_d_word)
    print('DEBUG: reduced query ' + str(cmd))
    d_word = cmd[0]
    if d_word in accepted_d_word:
        ans.success, ans.error_code = accepted_d_word[d_word](cmd[1:])
    else:
        ans.success = False
        ans.error_code = 0
    return ans


# initialize the rosnode and services
rospy.init_node('knowledge_base')
query_handler = rospy.Service('KBase/query', Query, handle_query)
data_handler = rospy.Service('KBase/data', Data, handle_data)

print('KBase ready!')
rospy.spin()
