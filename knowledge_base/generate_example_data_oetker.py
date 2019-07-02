from knowledge_base.Classes import *
import mongoengine as me
from utils import save_complete_db
import xml.etree.ElementTree as ET
from xml.dom import minidom

import sys



#Lists to add your entries to
objs = []


# load annotation file. general stuff (argument handling etc)
args = sys.argv
if len(args) < 2:
    print('Usage: python generate_example_data_oetker.py <DatabaseName> ')
    sys.exit()

db = me.connect(args[1], host="127.0.0.1", port=27018)
db.drop_database(args[1])

inputstr = ''



##################################################################################################################################################################

##Data which shall be put into the database
## Modifiy at will

#Objects-Entries
#categorys:
#container, food, cleaning stuff, drink, cutlery, snack
objs.append(Rcobject(name="kraft futter",         category='food', color="green",              shape="rectangular", size='4', weight='2'))
objs.append(Rcobject(name="erdnuesse",        category='food', color="green and red",           shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="saft",     category='drink', color="green and white",             shape="cylindrical", size='2', weight='5'))
objs.append(Rcobject(name="cola",           category='drink', color="red",                    shape="cylindrical", size='2', weight='4'))
objs.append(Rcobject(name="wasser",          category='drink', color="light blue",             shape="cylindrical", size='2', weight='5'))

#Crowd-entries
#dummys, overwritten by reportGroup

######################################################################################################################

# another check or sanity, this time for objects
object_names = []
for obj in objs:
    if obj.name in object_names:
        print('Object \"' + obj.name + '\" seems to appear at least two times! Exiting now!')
        exit(1)



#match read annotations to rooms, locations and doors

arena_rooms = []
arena_doors = []
arena_locations = []

#
arena = Arena(rooms=arena_rooms, doors=arena_doors, locations=arena_locations)
crowd = Crowd(persons=[])
rcobjects = Rcobjects(rcobjects=objs)

kbase = Kbase(arena=arena, crowd=crowd, rcobjects=rcobjects, identifier='TestKBase')


#print('DEBUG: toxml ')
bla = kbase.to_xml()
#print(minidom.parseString(ET.tostring(kbase.to_xml(), encoding='utf-8')).toprettyxml(indent="   "))

save_complete_db(kbase)
exit(0)
