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
    if ':' not in anno.get('label') or('room' not in anno.get('label') and 'location' not in anno.get('label')):
        print('Annotation \"' + anno.get('label') + '\" seems not to follow naming convention! Regex: (room|location):*name*')
        exit(1)
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
kitchen = Room(name='kitchen', numberofdoors='1')
fridge = Location(name='fridge', room=kitchen, isbeacon='True', isplacement='True')
kitchencounter = Location(name='kitchen counter', room=kitchen, isbeacon='True', isplacement='True')
bar = Location(name='bar', room=kitchen, isbeacon='True', isplacement='True')
cabinet = Location(name='cabinet', room=kitchen, isbeacon='True', isplacement='True')
sink = Location(name='sink', room=kitchen, isbeacon='True', isplacement='True')
stove = Location(name='stove', room=kitchen, isbeacon='True', isplacement='True')
arena_rooms.append(kitchen)
arena_locations.append(fridge)
arena_locations.append(kitchencounter)
arena_locations.append(bar)
arena_locations.append(cabinet)
arena_locations.append(sink)
arena_locations.append(stove)

livingroom = Room(name='living room', numberofdoors='2')
livingtable = Location(name='living table', room=livingroom, isbeacon='True', isplacement='True')
sofa = Location(name='sofa', room=livingroom, isbeacon='True', isplacement='True')
comfychair = Location(name='comfy chair', room=livingroom, isbeacon='True', isplacement='True')
arena_rooms.append(livingroom)
arena_locations.append(livingtable)
arena_locations.append(sofa)
arena_locations.append(comfychair)

corridor = Room(name='corridor', numberofdoors='3')
arena_rooms.append(corridor)

bathroom = Room(name='bath room', numberofdoors='1')
arena_rooms.append(bathroom)

outside = Room(name='outside', numberofdoors='1')
arena_rooms.append(outside)

d_outside_corridor = Door(roomone=corridor, roomtwo=outside)
arena_doors.append(d_outside_corridor)
d_bathroom_corridor = Door(roomone=bathroom, roomtwo=corridor)
arena_doors.append(d_bathroom_corridor)
d_livingroom_kitchen = Door(roomone=kitchen, roomtwo=livingroom)
arena_doors.append(d_livingroom_kitchen)
d_corridor_livingroom = Door(roomone=corridor, roomtwo=livingroom)
arena_doors.append(d_corridor_livingroom)

#Objects-Entries
#categorys:
#container, food, cleaning stuff, drink, cutlery, snack
objs.append(Rcobject(name="basket",         category='container', color="green",             location=livingtable, shape="rectangular", size='4', weight='2'))
objs.append(Rcobject(name="cereals",        category='food', color="green and red",          location=kitchencounter, shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="cloth",          category='cleaning stuff', color="yellow green or blue",  location=cabinet, shape="quite flat", size='4', weight='1'))
objs.append(Rcobject(name="coconut milk",     category='drink', color="green and white",            location=bar, shape="cylindrical", size='2', weight='5'))
objs.append(Rcobject(name="coke",           category='drink', color="red",                   location=bar, shape="cylindrical", size='2', weight='4'))
objs.append(Rcobject(name="cornflakes",     category='food', color="green white and red",    location=kitchencounter, shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="noodles",        category='food', color="yellow and black",       location=kitchencounter, shape="baggy", size='1', weight='1'))
objs.append(Rcobject(name="orange drink",   category='drink', color="blue and orange",       location=bar, shape="boxy", size='1', weight='3'))
objs.append(Rcobject(name="peas",           category='food', color="green and black",        location=kitchencounter, shape="cylindrical", size='1', weight='3'))
objs.append(Rcobject(name="plate",          category='cutlery', color="white",             location=cabinet, shape="that of a flat bowl", size='4', weight='1'))
objs.append(Rcobject(name="pringles",       category='snack', color="yellow",                location=sofa, shape="cylindrical", size='4', weight='3'))
objs.append(Rcobject(name="red bowl",       category='container', color="red",               location=livingtable, shape="that of a deep plate", size='2', weight='2'))
objs.append(Rcobject(name="salt",           category='food', color="black and blue",         location=kitchencounter, shape="cylindrical", size='0', weight='2'))
objs.append(Rcobject(name="soap",         category='cleaning stuff', color="light green",  location=sink, shape="rather boxy", size='2', weight='2'))
objs.append(Rcobject(name="sponge",         category='cleaning stuff', color="light green",  location=sink, shape="rather boxy", size='0', weight='1'))
objs.append(Rcobject(name="tomato pasta",   category='food', color="red and green",          location=kitchencounter, shape="that of a toothpaste tube", size='2', weight='2'))
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
