from Classes import *
import mongoengine as me
from utils import save_complete_db, add_annotation
import xml.etree.ElementTree as ET

import sys



#Lists to add your entries to
arena_rooms = []
arena_locations = []
arena_doors = []
objs = []
pers = []


# load annotation file. general stuff (argument handling etc)
args = sys.argv
if len(args) < 3:
    print('Usage: python generate_example_data.py <DatabaseName> <AnnotationFile>')
    sys.exit()

db = me.connect(args[1], host="127.0.0.1", port=27018)
db.drop_database(args[1])

inputstr = ''

with open(args[2], 'r') as f:
    inputstr = f.read()

annotations = [] # list where the xml annotations will be saved

#add those annotations to the list
annotationTree = ET.fromstring(inputstr)
for annotation in annotationTree.getchildren():
    if annotation.tag == 'ANNOTATION':
        annotations.append(annotation)

# check input for sanity
bdo_names = []
for anno in annotations:
    anno_name = anno.get('label').split(':')[1]
    if anno_name in bdo_names:
        print('Annotation \"' + anno_name + '\" seems to appear at least two times! Exiting now!')
        exit(1)
    bdo_names.append(anno_name)

##################################################################################################################################################################

##Data which shall be put into the database
## Modifiy at will

#Arena-entries (locations, rooms etc)
#<N_placementTwo> = (dinner table) | cabinet | bookshelf | (kitchen counter) | sofa | (couch table) | (side table) | (stove) | bed | closet | desk | bar;
corridor = Room(name='corridor', numberofdoors='0')
arena_rooms.append(corridor)


livingroom = Room(name='living room', numberofdoors='0')
arena_rooms.append(livingroom)


trophyroom = Room(name='trophy room', numberofdoors='0')
grasp = Location(name='grasp', room=trophyroom, isbeacon='True', isplacement='True')
arena_rooms.append(trophyroom)
arena_locations.append(grasp)

kitchen = Room(name='kitchen', numberofdoors='0')
counter = Location(name='counter', room=kitchen, isbeacon='True', isplacement='True')
arena_rooms.append(kitchen)
arena_locations.append(counter)


outside = Room(name='outside', numberofdoors='0')
arena_rooms.append(outside)


#Objects-Entries
#categorys:
#container, food, cleaning stuff, drink, cutlery, snack



#Crowd-entries
#dummys, overwritten by reportGroup

######################################################################################################################

# another check or sanity, this time for objects

#match read annotations to rooms, locations and doors

arena_rooms = [add_annotation(x, annotations) for x in arena_rooms]
arena_doors = [add_annotation(x, annotations) for x in arena_doors]
arena_locations = [add_annotation(x, annotations) for x in arena_locations]

#
arena = Arena(rooms=arena_rooms, doors=arena_doors, locations=arena_locations)
crowd = Crowd(persons=pers)
rcobjects = Rcobjects(rcobjects=objs)

kbase = Kbase(arena=arena, crowd=crowd, rcobjects=rcobjects, identifier='TestKBase')


#print('DEBUG: toxml ')
bla = kbase.to_xml()
#print(minidom.parseString(ET.tostring(kbase.to_xml(), encoding='utf-8')).toprettyxml(indent="   "))

save_complete_db(kbase)
exit(0)
