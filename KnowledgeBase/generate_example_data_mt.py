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
kitchen = Room(name='kitchen', numberofdoors='1')
cupboard = Location(name='cupboard', room=kitchen, isplacement='True')
storagetable = Location(name='storage table', room=kitchen, isplacement='True')
dishwasher = Location(name='dishwasher', room=kitchen, isbeacon='True', isplacement='True')
sink = Location(name='sink', room=kitchen, isbeacon='True', isplacement='True')
counter = Location(name='counter', room=kitchen, isbeacon='True', isplacement='True')
arena_rooms.append(kitchen)
arena_locations.append(cupboard)
arena_locations.append(storagetable)
arena_locations.append(dishwasher)
arena_locations.append(sink)
arena_locations.append(counter)

livingroom = Room(name='living room', numberofdoors='2')
endtable = Location(name='end table', room=livingroom, isplacement='True')
couch = Location(name='couch', room=livingroom, isbeacon='True')
bookcase = Location(name='bookcase', room=livingroom, isbeacon='True')
arena_rooms.append(livingroom)
arena_locations.append(endtable)
arena_locations.append(couch)
arena_locations.append(bookcase)

corridor = Room(name='corridor', numberofdoors='1')
arena_rooms.append(corridor)

bedroom = Room(name='bedroom', numberofdoors='2')
sidetable = Location(name='side table', room=bedroom, isbeacon='True')
bed = Location(name='bed', room=bedroom, isplacement='True')
desk = Location(name='desk', room=bedroom, isplacement='True')
arena_rooms.append(bedroom)
arena_locations.append(sidetable)
arena_locations.append(bed)
arena_locations.append(desk)

diningroom = Room(name='dining room', numberofdoors='0')
diningtable = Location(name='dining table', room=diningroom, isplacement='True')
arena_rooms.append(diningroom)
arena_locations.append(diningtable)

outside = Room(name='outside', numberofdoors='2')
exit = Location(name='exit', room=outside, isbeacon='True', ishidden=True)
arena_rooms.append(outside)
arena_locations.append(exit)

d_corridor_outside = Door(roomone=corridor, roomtwo=outside)
arena_doors.append(d_corridor_outside)
d_livingroom_outside = Door(roomone=livingroom, roomtwo=outside)
arena_doors.append(d_livingroom_outside)
d_livingroom_bedroom = Door(roomone=livingroom, roomtwo=bedroom)
arena_doors.append(d_livingroom_bedroom)
d_kitchen_bedroom = Door(roomone=kitchen, roomtwo=bedroom)
arena_doors.append(d_kitchen_bedroom)


inspectionpoint = Location(name='inspection point', room=livingroom, ishidden=True)
inspectionend = Location(name='inspection end', room=corridor, ishidden=True)
helpmecarrystart = Location(name='help me carry start', room=livingroom, ishidden=True)
cocktailpartystart = Location(name='cocktail party start', room=livingroom, ishidden=True)
partyarea = Location(name='party area', room=livingroom, ishidden=True)
gpsrstarta = Location(name='gpsr start a', room=livingroom, ishidden=True)
gpsrstartb = Location(name='gpsr start b', room=bedroom, ishidden=True)
tourguide = Location(name='tourguide', room=bedroom, ishidden=True)
arena_locations.append(inspectionpoint)
arena_locations.append(inspectionend)
arena_locations.append(helpmecarrystart)
arena_locations.append(cocktailpartystart)
arena_locations.append(partyarea)
arena_locations.append(gpsrstarta)
arena_locations.append(gpsrstartb)
arena_locations.append(tourguide)


#Objects-Entries
#categorys:
#container, food, cleaning stuff, drink, cutlery, snack
objs.append(Rcobject(name="cloth",         category='cleaning stuff', color="orange",             location=sidetable, shape="quite flat", size='4', weight='1'))
objs.append(Rcobject(name="scrubby",        category='cleaning stuff', color="yellow and green",          location=sidetable, shape="boxy", size='2', weight='1'))
objs.append(Rcobject(name="sponge",          category='cleaning stuff', color="pink",  location=sidetable, shape="boxy", size='3', weight='1'))
objs.append(Rcobject(name="basket",     category='containers', color="white",            location=endtable, shape="boxy", size='5', weight='4'))
objs.append(Rcobject(name="tray",           category='containers', color="white",                   location=endtable, shape="quadratic and flat", size='5', weight='4'))
objs.append(Rcobject(name="chocolate drink",     category='drinks', color="white and brown",    location=counter, shape="cylindrical", size='3', weight='4'))
objs.append(Rcobject(name="coke",        category='drinks', color="red",       location=counter, shape="cylindrical", size='2', weight='3'))
objs.append(Rcobject(name="grape juice",   category='drinks', color="white and red",       location=counter, shape="boxy", size='2', weight='3'))
objs.append(Rcobject(name="orange juice",           category='drinks', color="white and orange",        location=counter, shape="boxy", size='2', weight='3'))
objs.append(Rcobject(name="sprite",          category='drinks', color="blue",             location=counter, shape="cylindrical", size='2', weight='3'))
objs.append(Rcobject(name="cereal",       category='food', color="yellow",                location=cupboard, shape="boxy", size='3', weight='1'))
objs.append(Rcobject(name="noodles",       category='food', color="green and white",               location=cupboard, shape="boxy", size='3', weight='1'))
objs.append(Rcobject(name="sausages",           category='food', color="blue and red",         location=cupboard, shape="cylindrical", size='1', weight='2'))
objs.append(Rcobject(name="apple",         category='fruits', color="red or green",  location=bookcase, shape="round", size='1', weight='1'))
objs.append(Rcobject(name="orange",         category='fruits', color="orange",  location=bookcase, shape="round", size='1', weight='1'))
objs.append(Rcobject(name="paprika",   category='fruits', color="red",          location=bookcase, shape="rather round", size='2', weight='2'))
objs.append(Rcobject(name="crackers",          category='snacks', color="orange",            location=bookcase, shape="quadratic and flat", size='1', weight='1'))
objs.append(Rcobject(name="potato chips",          category='snacks', color="orange",            location=bookcase, shape="couldy", size='5', weight='3'))
objs.append(Rcobject(name="pringles",          category='snacks', color="green",            location=bookcase, shape="cylindrical", size='5', weight='3'))
objs.append(Rcobject(name="bowl",          category='kitchen stuff', color="green",            location=storagetable, shape="cylindrical and hollow", size='4', weight='1'))
objs.append(Rcobject(name="cup",          category='kitchen stuff', color="green",            location=storagetable, shape="cylindrical and hollow", size='4', weight='1'))
objs.append(Rcobject(name="fork",          category='kitchen stuff', color="green",            location=storagetable, shape="elongated", size='2', weight='1'))
objs.append(Rcobject(name="knife",          category='kitchen stuff', color="green",            location=storagetable, shape="elongated", size='2', weight='1'))
objs.append(Rcobject(name="plate",          category='kitchen stuff', color="green",            location=storagetable, shape="quite flat", size='4', weight='1'))
objs.append(Rcobject(name="spoon",          category='kitchen stuff', color="green",            location=storagetable, shape="elongated", size='2', weight='1'))




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
