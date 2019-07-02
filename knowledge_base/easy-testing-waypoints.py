#!/usr/bin/env python
# script for easier testing of the kbase

# dict to control which waypoints should be tested
tests = {'side table': 'main', 'dining room' : ''}

import rospy
from knowledge_base_msgs.srv import *
from knowledge_base.Classes import *
import xml.etree.ElementTree as ET
import mongoengine as me

db_run = me.connect('magdeburg_db', host="127.0.0.1", port=27018)


for location in tests:
    viewpoint = tests[location] or 'main'
    rospy.wait_for_service('KBase/query')
    try:
        retrieving = rospy.ServiceProxy('KBase/query', Query)
        resp1 = retrieving('where is the ' + location + ' ' + viewpoint)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        exit(1)

    if not resp1.success:
        print('The ' + location + ' with viepoint ' + viewpoint + ' could NOT be found!')
    else:
        print('The ' + location + ' with viepoint ' + viewpoint + ' seems ok!')


exit(0)
