from Classes import *
import mongoengine as me
from utils import save_complete_db, add_annotation
import xml.etree.ElementTree as ET
from xml.dom import minidom

import sys


#TEST if local github works

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

livingroom = Room(name='living room', numberofdoors='0')
tvtable = Location(name='tv table', room=livingroom, isplacement=True)
cupboard = Location(name='cupboard', room=livingroom, isplacement=True)
couchtable = Location(name='couch table', room=livingroom, isbeacon=True, isplacement=True)
couch = Location(name='couch', room=livingroom)
arena_rooms.append(livingroom)
arena_locations.append(tvtable)
arena_locations.append(cupboard)
arena_locations.append(couch)
arena_locations.append(couchtable)

bedroom = Room(name='bedroom', numberofdoors='2')
bed = Location(name='bed', room=bedroom, isbeacon=True)
desk = Location(name='desk', room=bedroom, isplacement=True)
bookcase = Location(name='bookcase', room=bedroom, isplacement=True)
sidetable = Location(name='side table', room=bedroom, isplacement=True)
arena_rooms.append(bedroom)
arena_locations.append(bed)
arena_locations.append(desk)
arena_locations.append(bookcase)
arena_locations.append(sidetable)

kitchen = Room(name='kitchen', numberofdoors='0')
sink = Location(name='sink', room=kitchen)
kitchentable = Location(name='kitchen table', room=kitchen, isplacement=True)
kitchencabinet = Location(name='kitchen cabinet', room=kitchen, isplacement=True)
bar = Location(name='bar', room=kitchen, isbeacon=True, isplacement=True)
arena_rooms.append(kitchen)
arena_locations.append(sink)
arena_locations.append(kitchentable)
arena_locations.append(kitchencabinet)
arena_locations.append(bar)

diningroom = Room(name='dining room', numberofdoors='2')
diningtable = Location(name='dining table', room=diningroom, isplacement=True, isbeacon=True)
cabinet = Location(name='cabinet', room=diningroom, isplacement=True)
displaycase = Location(name='display case', room=diningroom, isplacement=True)
storageshelf = Location(name='storage shelf', room=diningroom, isplacement=True)
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
objs.append(Rcobject(name="shower gel",         category='care', color="pink",             location=bookcase, shape="smooth", size='2', weight='3'))
objs.append(Rcobject(name="soap",         category='care', color="white",             location=bookcase, shape="rectangular", size='1', weight='1'))
objs.append(Rcobject(name="toothpaste",         category='care', color="green",             location=bookcase, shape="like a tube", size='2', weight='1'))

objs.append(Rcobject(name="sponge",         category='cleaning stuff', color="yellow and green",             location=kitchencabinet, shape="boxy", size='1', weight='0'))
objs.append(Rcobject(name="wiper",         category='cleaning stuff', color="yellow",             location=kitchencabinet, shape="flat", size='3', weight='0'))

objs.append(Rcobject(name="tray",         category='container', color="white",             location=cupboard, shape="boxy", size='4', weight='2'))
objs.append(Rcobject(name="box",         category='container', color="yellow and white",             location=cupboard, shape="boxy", size='4', weight='2'))

objs.append(Rcobject(name="cacao",         category='drinks', color="brown",             location=kitchentable, shape="boxy", size='4', weight='8'))
objs.append(Rcobject(name="coke",         category='drinks', color="red",             location=kitchentable, shape="cylindrical", size='2', weight='3'))
objs.append(Rcobject(name="malz",         category='drinks', color="black and red",             location=kitchentable, shape="like a bottle", size='3', weight='5'))
objs.append(Rcobject(name="mixdrink",         category='drinks', color="red and yellow",             location=kitchentable, shape="cylindrical", size='2', weight='3'))
objs.append(Rcobject(name="orange juice",         category='drinks', color="orange",             location=kitchentable, shape="like a stepped upon bottle", size='2', weight='3'))
objs.append(Rcobject(name="peppermint tea",         category='drinks', color="gren and white",             location=kitchentable, shape="boxy", size='3', weight='1'))
objs.append(Rcobject(name="water",         category='drinks', color="blue and see through",             location=kitchentable, shape="like a bottle", size='3', weight='5'))

objs.append(Rcobject(name="cookies",         category='snacks', color="light blue",             location=couchtable, shape="rectangular", size='3', weight='3'))
objs.append(Rcobject(name="fruit bar",         category='snacks', color="green and red",             location=couchtable, shape="rectangular", size='2', weight='1'))
objs.append(Rcobject(name="kinder joy",         category='snacks', color="red and white",             location=couchtable, shape="rectangular", size='1', weight='1'))
objs.append(Rcobject(name="nuts",         category='snacks', color="yellow and purple",             location=couchtable, shape="rectangular", size='2', weight='1'))

objs.append(Rcobject(name="apple",         category='food', color="green",             location=cabinet, shape="rectangular", size='2', weight='2'))
objs.append(Rcobject(name="green paprika",         category='food', color="green",             location=cabinet, shape="rectangular", size='2', weight='2'))
objs.append(Rcobject(name="kiwi",         category='food', color="brownish green",             location=cabinet, shape="rectangular", size='1', weight='1'))
objs.append(Rcobject(name="lemon",         category='food', color="yellow",             location=cabinet, shape="rectangular", size='1', weight='1'))
objs.append(Rcobject(name="noodles",         category='food', color="yellow and green",             location=cabinet, shape="rectangular", size='3', weight='5'))
objs.append(Rcobject(name="pepper",         category='food', color="black",             location=cabinet, shape="rectangular", size='2', weight='1'))
objs.append(Rcobject(name="salt",         category='food', color="white and blue",             location=cabinet, shape="rectangular", size='2', weight='5'))
objs.append(Rcobject(name="tomato paste",         category='food', color="red and green",             location=cabinet, shape="rectangular", size='2', weight='2'))

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
