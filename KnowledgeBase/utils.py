from Classes import *


def retrieve_object_by_identifier(name):
    '''

    :param name:
    :return:
    '''
    all_entrys = list(Person.objects(name=name)) + \
                 list(Location.objects(name=name)) + \
                 list(Room.objects(name=name)) + \
                 list(Rcobject.objects(name=name)) + \
                 list(Person.objects(uuid=name))
    if len(all_entrys) < 1:
        print('Failed! Found no person, location, room or RCObject with name ' + name)
        return None
    if len(all_entrys) > 1:
        print('Warning! Found more than one person, location, room or RCObject with name ' +
              name)
    return all_entrys[0]


def filter_fillwords(query):
    '''
    Filters some fillerwords out of a query.
    :param query: the unfiltered query as a list, split by space
    :return: the filtered query as a list, split by space
    '''
    fillwords = ['are', 'is', 'was', 'the', 'of', 'that', 'were', 'have', 'has', 'a', 'an', 'in', 'at', 'on', 'around']
    ret_query = [x for x in query if x not in fillwords]
    return ret_query


def save_complete_db(kbase):
    for room in kbase.arena.rooms:
        room.save()
    for location in kbase.arena.locations:
        location.save()
    for door in kbase.arena.doors:
        door.save()
    for obj in kbase.rcobjects.rcobjects:
        obj.save()
    for per in kbase.crowd.persons:
        per.save()

    kbase.arena.save()
    kbase.crowd.save()
    kbase.rcobjects.save()
    kbase.save()


def add_annotation(arenaobj, annotations_xml):
    loc_type = ''
    xml_identifier = ''
    if type(arenaobj) is Room:
        loc_type = 'room'
        xml_identifier = arenaobj.name
    elif type(arenaobj) is Location:
        loc_type = 'location'
        xml_identifier = arenaobj.name
    elif type(arenaobj) is Door:
        loc_type = 'door'
        xml_identifier = arenaobj.roomOne.name + '_' + arenaobj.roomTwo.name

    annot = Annotation()
    annot.label = xml_identifier
    vps = []
    for annot_xml in annotations_xml:
        if annot_xml.get('label') == loc_type + ':' + xml_identifier:
            poly = False
            vp_main = False
            for annotChild in annot_xml.getchildren():
                if annotChild.tag == 'VIEWPOINT':
                    if annotChild.get('label') == 'main':
                        vp_main = True
                    vp = Viewpoint.from_xml(annotChild)
                    vps.append(vp)
                elif annotChild.tag == 'PRECISEPOLYGON':
                    poly = True
                    points = []
                    for point2d in annotChild.getchildren():
                        if point2d.tag == 'POINT2D':
                            point = Point2d.from_xml(point2d)
                            points.append([point.x, point.y])
                    points.append(points[0]) #polygon needs to begin and end at same location
                    annot.polygon = [points]
            if not poly:
                print('Polygon from ' + xml_identifier + ' is missing.')
            if not vp_main:
                print('ViewPoint \'main\' from ' + xml_identifier + ' is missing.')
    annot.viewpoints = vps
    arenaobj.annotation = annot
    return arenaobj


def get_class_of_bdo(bdo):
    class_of_bdo = None
    if bdo == 'rcobject' or bdo == 'rcobjects' or bdo == 'object' or bdo == 'objects':
        class_of_bdo = Rcobject
    elif bdo == 'person' or bdo == 'persons':
        class_of_bdo = Person
    elif bdo == 'location' or bdo == 'locations':
        class_of_bdo = Location
    elif bdo == 'room' or bdo == 'rooms':
        class_of_bdo = Room
    elif bdo == 'door' or bdo == 'doors':
        class_of_bdo = Door
    return class_of_bdo


def aquire_xml_in_string(string):
    '''

    :param string:
    :return: a tuple of two ints, corresponding to the positions in the string where the xml starts and ends
    '''
    start = string.find('<')
    end = string.rfind('>')+1
    return start, end


def reduce_query(query_string, accepted_w_words):
    query_string = query_string.lower()
    # swich encoding from utf8 to ascii
    if type(query_string) == unicode:
        query_string = query_string.encode('ascii','replace')

    # check with which q_word the query starts and replace all of its ' ' with '%'
    for w_word in accepted_w_words:
        query_string = query_string.replace(w_word, w_word.replace(' ', '%'))

    # build a list with all names found in the database
    names =  [x.name for x in Rcobject.objects()]
    names += [x.name for x in Location.objects()]
    names += [x.name for x in Room.objects()]
    names += [x.name for x in Person.objects()]

    # check if the query contains any of those names
    # if yes, replace them with a version where all ' ' are replaced with '%'
    for name in names:
        query_string = query_string.replace(name, name.replace(' ', '%'))

    # check for xml
    xml_replacement = 'xml_replace'
    xml = ''
    if '<' in query_string and '>' in query_string:
        start, end = aquire_xml_in_string(query_string)
        xml = query_string[start:end]
        query_string = query_string[:start] + xml_replacement + query_string[end:]

    # then split the query as before by ' '
    query_list = query_string.split(' ')

    # filter the fillerwords
    query_list = filter_fillwords(query_list)

    # then iterate through the query and replace all '_' with '%' again and 'xml_replace' with the actual xml
    query_list = [query.replace(xml_replacement, xml).replace('%', ' ') for query in query_list]

    # also try not to destroy any xml which may be given
    # smarter way for future: create a sentence-metric with which you could determine the kind of question given (1) and
    # also which parts are most likely important compounds, e.g. a persons first and sir name (2)
    return query_list
