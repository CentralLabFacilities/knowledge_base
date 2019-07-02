from knowledge_base.Classes import *
import xml.etree.ElementTree as ET
from knowledge_base.utils import retrieve_object_by_identifier, get_class_of_bdo
from mongoengine.queryset.visitor import Q

def str_to_xml(str):
    # TODO: rewrite proper
    return '<STRING val="' + str + '"/>'


def int_to_xml(int):
    # TODO: rewrite proper
    return '<INT val="' + str(int) + '"/>'


def float_to_xml(float):
    # TODO: rewrite proper
    return '<FLOAT val="' + str(float) + '"/>'


def handle_who(query):
    '''
    Hander for the question word who. Will return a xml-ified Person.
    :param query:
    :return:
    '''
    # query is list with one element, which is a identifier for a person
    # TODO: filter wrong querries
    name = query[0]
    pers = retrieve_object_by_identifier(name)
    if type(pers) is not Person:
        bdo_types = [type(Rcobject), type(Door), type(Location), type(Room)]
        if pers is None:
            return 'Failed, did not find a Person with name ' + name, 61
        if type(pers) in bdo_types:
            return 'Failed, did not find a Person with name ' + name + ' but an ' + str(type(pers)), 62
    return ET.tostring(pers.to_xml()), 0


def handle_what(query):
    '''

    :param query:
    :return:
    '''
    # query is either list with one element ('[what] cup'), so we return a object
    # or with two elements ('[what] shape cup'), so we return the attribute of the object as string
    # TODO: filter wrong querries
    name = query[-1]
    obj = retrieve_object_by_identifier(name)
    if type(obj) is not Rcobject:
        if obj is None:
            return 'Failed, did not find an object with name ' + name, 11
        else:
            return 'Failed, did not find an object with name ' + name + ' but an ' + str(type(obj)), 12
    if len(query) > 1:
        attr = query[0]
        attribs = {x: obj.__getattribute__(x) for x in obj._fields}
        ans = attribs[attr]
        if type(ans) == float:
            return float_to_xml(ans)
        elif type(ans) == int:
            return int_to_xml(ans)
        elif type(ans) == unicode:
            return str_to_xml(ans.encode('ascii','replace'))
        elif type(ans) == Location:
            return str_to_xml(ans.name)
        return 'Failed, type of attribute ' + attr + ' is ' + str(type(ans)) +', and there is no xml-ifier for that!', 13

    return ET.tostring(obj.to_xml()), 0


def handle_where(query):
    '''

    :param query:
    :return:
    '''
    # query is a list with one element, which is the unique identifier of either a location, person, room or
    # object. It may have a second element, which would be a unique identifier for one of many
    # viewpoints a location or room may have
    # TODO: filter wrong querries
    name = query[0]
    viewpoint_name = None
    if len(query) > 1:
        viewpoint_name = query[1]
    entry = retrieve_object_by_identifier(name)

    if not entry:
        return 'Failed! Found no person, location, room or RCObject with name ' + name, 21

    # retrieve annotation of the fetched thingy
    annot = None
    if type(entry) == Room or type(entry) == Location:
        annot = entry.annotation
    elif type(entry) == Person:
        return ET.tostring(entry.position.to_xml()), 0 # persons have a position themselves
        #  so we do not need to go over annot
    elif type(entry) == Rcobject:
        annot = entry.location.annotation

    # retrieve viewpoint
    viewpoints = None
    if viewpoint_name:
        viewpoints = [vp for vp in annot.viewpoints if vp.label == viewpoint_name]
    else:
        viewpoints = [vp for vp in annot.viewpoints if vp.label == 'main']
    if not viewpoints:
        return 'Failed! Found no viewpoint with name ' + str(viewpoint_name), 21
    
    viewpoint = viewpoints[0]

    return ET.tostring(viewpoint.to_xml()), 0


def handle_in_which(query):
    '''
    query is a list with 3-4 elements for which the second element is always either 'location' or 'room' and the
    third is either the keyword 'point' or a unique identifier of either a location, person, room or object. In the case
    the third element is 'point', a Point2D in xml format should follow as the third element.
    :param query:
    :return:
    '''
    # TODO: filter wrong querries

    # if there is a point in the query, parse it into point2D
    point = None
    if len(query) > 2 and query[1] == 'point':
        point = Point2d.from_xml(ET.fromstring(query[2]))

    # retrieve thingy by identifier if we dont already have a point
    if not point:
        entry = retrieve_object_by_identifier(query[1])
        if not entry:
            return 'Failed! Found no person, location, room or RCObject with name ' + query[1], 31

        # now there are 4 possibilities: we have retrieved a person (->point), location, room or object
        if type(entry) == Person:
            point = entry.position.point2d


        elif type(entry) == Location:
            if query[0] == 'room':
                return ET.tostring(entry.room.to_xml()), 0
            elif query[0] == 'location':
                return ET.tostring(entry.to_xml()), 0


        elif type(entry) == Room:
            if query[0] == 'room':
                return ET.tostring(entry.to_xml()), 0
            elif query[0] == 'location':
                print('Failed, query ' + ' '.join(query) + ' makes no sense! A room cannot be in a location.')
                return 'Failed, a room cannot be in a location!', 32


        elif type(entry) == Rcobject:
            if query[0] == 'room':
                return ET.tostring(entry.location.room.to_xml()), 0
            elif query[0] == 'location':
                return ET.tostring(entry.location.to_xml()), 0

    # for persons and given points we need to keep going
    ## retrieve room/ location in which this point lies


    if query[0] == 'room':
        for room in Room.objects(annotation__polygon__geo_intersects=[point.x, point.y]):
            return ET.tostring(room.to_xml()), 0
    elif query[0] == 'location':
        for loc in Location.objects(ishidden=False, annotation__polygon__geo_intersects=[point.x, point.y]):
            return ET.tostring(loc.to_xml()), 0

    print('Failed, query ' + ' '.join(query) + ' could not find a corresponding item!')
    return 'Failed, something unforseen happened, maybe the there is no room/location this point/object/location/room/person lies in', 33


def handle_which(query):
    '''
    query is a list with length 3. first element is either location, room, rcobject or person, second element is a
    attribute of the class of the first element. the third element is a value that this attribute shall have to be
    retrieved
    :param query:
    :return:
    '''
    # TODO: filter wrong querries
    # get class of searched after elements
    class_of_bdo = get_class_of_bdo(query[0])
    if not class_of_bdo:
        return 'Failed, class ' + query[0] + ' is no viable BDO!', 41
    # get attribute for which the number of distinct elements shall be found
    complex_attributes = ['room', 'location']
    attribute_of_class = query[1]
    value = query[2]
    advanced_query = None
    if attribute_of_class in complex_attributes:
        rloc_class = None
        if attribute_of_class == 'room':
            rloc_class = Room
            value = rloc_class.objects(name=value).get()
            if class_of_bdo == Door:
                rloc_class = Door
                advanced_query = Q(roomone=value) or Q(roomtwo=value)
        elif attribute_of_class == 'location':
            rloc_class = Location
            value = rloc_class.objects(name=value).get()
    method_parameter_dict = {attribute_of_class : value}
    if class_of_bdo is Location:
        method_parameter_dict['ishidden'] = False
    if not advanced_query:
        list_of_searched_bdo = class_of_bdo.objects(**method_parameter_dict)
    else:
        list_of_searched_bdo = class_of_bdo.objects(advanced_query)


    # prepare root node for list
    root_node = None
    if class_of_bdo == Person:
        root_node = ET.Element('PERSONDATALIST')
    elif class_of_bdo == Rcobject:
        root_node = ET.Element('RCOBJECTLIST')
    elif class_of_bdo == Room:
        root_node = ET.Element('ROOMLIST')
    elif class_of_bdo == Location:
        root_node = ET.Element('LOCATIONLIST')
    elif class_of_bdo == Door:
        root_node = ET.Element('DOORLIST')

    for obj in list_of_searched_bdo:
        root_node.append(obj.to_xml())

    # Generator stuff for btl-xml...
    gen = ET.SubElement(root_node, 'GENERATOR')
    gen.text = 'Kbase'
    time = ET.SubElement(root_node, 'TIMESTAMP')
    inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
    updated = ET.SubElement(time, 'UPDATED', {'value': '1'})

    ret_str = ET.tostring(root_node)
    return ret_str, 0


def handle_how_many(query):
    '''
    query is a list of length 2. the second element is either location, room, rcobject or person. the first element is
    a attribute of the first element.
    :param query:
    :return:
    '''
    # TODO: filter wrong querries
    # get class of searched after elements
    class_of_bdo = get_class_of_bdo(query[1])
    if not class_of_bdo:
        print('Failed, ' + query[1] + ' is no valid class for how many!')
        return 'Failed, ' + query[1] + ' is no valid class for how many!', 51

    # get attribute for which the number of distinct elements shall be found
    attribute_of_class = query[0]
    location_hider = {}
    if class_of_bdo == Location:
        location_hider['ishidden'] = False
    distinct = class_of_bdo.objects(**location_hider).distinct(attribute_of_class)
    return int_to_xml(len(distinct)), 0


def handle_get(query):
    '''
    Method to get a non-basic object. query is always a list of exactly one element, which can be 'kbase', 'rcobjects',
    'crowd', 'arena' or 'context'.
    :param query:
    :return:
    '''
    # TODO: filter wrong querries
    if query[0] == 'kbase':
        return ET.tostring(Kbase.objects()[0].to_xml()), 0
    elif query[0] == 'arena':
        return ET.tostring(Kbase.objects()[0].arena.to_xml()), 0
    elif query[0] == 'rcobjects' or query[0] == 'objects':
        return ET.tostring(Kbase.objects()[0].rcobjects.to_xml()), 0
    elif query[0] == 'crowd':
        return ET.tostring(Kbase.objects()[0].crowd.to_xml()), 0

    error_str = 'Failed, query get ' + query[0] + ' could not be answered! Please ask for kbase, arena, (rc)objects or crowd!'

    print(error_str)
    return error_str, 71

#################### low prio:

def handle_when(query):
    # TODO: filter wrong querries
    pass


def handle_show(query):
    # TODO: filter wrong querries
    pass
