from Classes import *
import mongoengine as me
from utils import save_complete_db, add_annotation
import xml.etree.ElementTree as ET
from xml.dom import minidom

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

livingroom = Room(name='living room', numberofdoors='0')
tvtable = Location(name='tv table', room=livingroom, isplacement=True)
cupboard = Location(name='cupboard', room=livingroom, isplacement=True)
couch = Location(name='couch', room=livingroom, isbeacon='True', isplacement=True)
couchtable = Location(name='couch table', room=livingroom)
arena_rooms.append(livingroom)
arena_locations.append(tvtable)
arena_locations.append(cupboard)
arena_locations.append(couch)
arena_locations.append(couchtable)

bedroom = Room(name='bedroom', numberofdoors='2')
bed = Location(name='bed', room=bedroom, isbeacon=True)
desk = Location(name='desk', room=bedroom, isplacement=True)
bookcase = Location(name='bookcase', room=bedroom, isplacement=True)
bedsidetable = Location(name='bedside table', room=bedroom, isplacement=True)
arena_rooms.append(bedroom)
arena_locations.append(bed)
arena_locations.append(desk)
arena_locations.append(bookcase)
arena_locations.append(bedsidetable)

kitchen = Room(name='kitchen', numberofdoors='0')
sink = Location(name='sink', room=kitchen, isbeacon='True')
kitchentable = Location(name='kitchen table', room=kitchen, isplacement=True)
kitchencabinet = Location(name='kitchen cabinet', room=kitchen, isplacement=True)
bar = Location(name='bar', room=kitchen, isbeacon='True', isplacement=True)
arena_rooms.append(kitchen)
arena_locations.append(sink)
arena_locations.append(kitchentable)
arena_locations.append(kitchencabinet)
arena_locations.append(bar)

diningroom = Room(name='dining room', numberofdoors='2')
diningtable = Location(name='dining table', room=diningroom, isplacement='True', isbeacon=True)
cabinet = Location(name='cabinet', room=diningroom, isplacement='True')
displaycase = Location(name='display case', room=diningroom, isplacement='True')
storageshelf = Location(name='storage shelf', room=diningroom, isplacement='True')
arena_rooms.append(diningroom)
arena_locations.append(diningtable)
arena_locations.append(cabinet)
arena_locations.append(displaycase)
arena_locations.append(storageshelf)

outside = Room(name='outside', numberofdoors='2')
arena_rooms.append(outside)

d_outside_diningroom = Door(roomone=diningroom, roomtwo=outside)
arena_doors.append(d_outside_diningroom)
d_bedroom_diningroom = Door(roomone=diningroom, roomtwo=bedroom)
arena_doors.append(d_bedroom_diningroom)
d_outside_bedroom = Door(roomone=bedroom, roomtwo=outside)
arena_doors.append(d_outside_bedroom)

#Objects-Entries
#categorys:
#container, food, cleaning stuff, drink, cutlery, snack
objs.append(Rcobject(name="basket",         category='container', color="green",             location=kitchentable, shape="rectangular", size='4', weight='2'))
objs.append(Rcobject(name="cereals",        category='food', color="green and red",          location=kitchentable, shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="cloth",          category='cleaning stuff', color="yellow green or blue",  location=cabinet, shape="quite flat", size='4', weight='1'))
objs.append(Rcobject(name="coconut milk",     category='drink', color="green and white",            location=bar, shape="cylindrical", size='2', weight='5'))
objs.append(Rcobject(name="coke",           category='drink', color="red",                   location=bar, shape="cylindrical", size='2', weight='4'))
objs.append(Rcobject(name="cornflakes",     category='food', color="green white and red",    location=kitchentable, shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="noodles",        category='food', color="yellow and black",       location=kitchentable, shape="baggy", size='1', weight='1'))
objs.append(Rcobject(name="orange drink",   category='drink', color="blue and orange",       location=bar, shape="boxy", size='1', weight='3'))
objs.append(Rcobject(name="peas",           category='food', color="green and black",        location=kitchentable, shape="cylindrical", size='1', weight='3'))
objs.append(Rcobject(name="plate",          category='cutlery', color="white",             location=cabinet, shape="that of a flat bowl", size='4', weight='1'))
objs.append(Rcobject(name="pringles",       category='snack', color="yellow",                location=kitchentable, shape="cylindrical", size='4', weight='3'))
objs.append(Rcobject(name="red bowl",       category='container', color="red",               location=kitchentable, shape="that of a deep plate", size='2', weight='2'))
objs.append(Rcobject(name="salt",           category='food', color="black and blue",         location=kitchentable, shape="cylindrical", size='0', weight='2'))
objs.append(Rcobject(name="soap",         category='cleaning stuff', color="light green",  location=sink, shape="rather boxy", size='2', weight='2'))
objs.append(Rcobject(name="sponge",         category='cleaning stuff', color="light green",  location=sink, shape="rather boxy", size='0', weight='1'))
objs.append(Rcobject(name="tomato pasta",   category='food', color="red and green",          location=kitchentable, shape="that of a toothpaste tube", size='2', weight='2'))
objs.append(Rcobject(name="water",          category='drink', color="light blue",            location=bar, shape="cylindrical", size='2', weight='5'))

#Crowd-entries
#dummys, overwritten by reportGroup

######################################################################################################################

# another check or sanity, this time for objects
object_names = []
for obj in objs:
    if obj.name in object_names:
        print('Object \"' + obj.name + '\" seems to appear at least two times! Exiting now!')
        exit(1)
    if obj.name in bdo_names:
        print('Object \"' + obj.name + '\" seems to be also a room-, location- or door-name! Exiting now!')
        exit(1)


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
