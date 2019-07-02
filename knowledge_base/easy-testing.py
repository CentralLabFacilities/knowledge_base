#!/usr/bin/env python
# script for easier testing of the kbase

# dict to control which tests should be
tests = {'saving': True, 'get kbase': True}

import rospy
from knowledge_base_msgs.srv import *
from knowledge_base.Classes import *
import xml.etree.ElementTree as ET
import mongoengine as me

db_run = me.connect('csra_db', host="127.0.0.1", port=27018)


if tests['saving']: # saving
    # get a location (the sink)
    print('Commencing Saving test')
    rospy.wait_for_service('KBase/query')
    try:
        retrieving = rospy.ServiceProxy('KBase/query', Query)
        resp1 = retrieving('in which location is the sink')
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        exit(1)

    if not resp1.success:
        print('First call returned unsuccessful!')
        exit(1)

    # change the theta of the main viewpoint to 1
    loc = Location.from_xml(ET.fromstring(resp1.answer))
    vp = [x for x in loc.annotation.viewpoints if x.label == 'main'][0]
    vp.positiondata.theta = 1

    # save the same thing again
    rospy.wait_for_service('KBase/data')
    try:
        saving = rospy.ServiceProxy('KBase/data', Data)
        resp2 = saving('remember ' + ET.tostring(loc.to_xml()))
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        exit(1)

    if not resp2.success:
        print('Second call returned unsuccessful!')
        exit(1)

    # get a location again (the sink)
    rospy.wait_for_service('KBase/query')
    try:
        retrieving = rospy.ServiceProxy('KBase/query', Query)
        resp1 = retrieving('in which location is the sink')
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        exit(1)

    if not resp1.success:
        print('Third call returned unsuccessful!')
        exit(1)

    # check if main theta is indeed 1
    loc = Location.from_xml(ET.fromstring(resp1.answer))
    vp = [x for x in loc.annotation.viewpoints if x.label == 'main'][0]
    assert vp.positiondata.theta == 1


if tests['get kbase']:
    # get the kbase (should be tested last, to be save everything is in a working order on kbase site)
    print('Commencing getting the kbase test')
    rospy.wait_for_service('KBase/query')
    try:
        retrieving = rospy.ServiceProxy('KBase/query', Query)
        resp1 = retrieving('get kbase')
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)
        exit(1)

    if not resp1.success:
        print('Call returned unsuccessful!')
        exit(1)


exit(0)
