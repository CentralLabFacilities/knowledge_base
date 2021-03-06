from knowledge_base.Classes import *
import xml.etree.ElementTree as ET
from knowledge_base.utils import retrieve_object_by_identifier, get_class_of_bdo, debug_print
import traceback


def handle_forget(data):
    '''
    Hander for the data word forget. Will delete a bdo from the knowledge base.
    :param data:
    :param delete_references
    :return:
    '''
    # data is list with one or two elements. if it is of length one, it will contain the unique identifier of the bdo
    # to delete. otherwise the first element shall be "all" and the second either "person(s)", "object(s)", "door(s)",
    # "location(s)" or "room(s)"
    # TODO: filter wrong querries
    if len(data) > 1:  # "all" path
        types = {'person' : Person,
                 'object' : Rcobject,
                 'rcobject' : Rcobject,
                 'room' : Room,
                 'location' : Location,
                 'door': Door}
        if not data[0] == 'all':
            print('More than one element for forget and first element not \"all\"')
            return False, 81
        if data[1] not in types:
            if data[1].endswith('s') and data[1][:-1] in types:  # got plural of type, e.g. persons
                data[1] = data[1][:-1]
            else:
                print('Identification word not in classes allowed to delete!')
                return False, 82
        types[data[1]].objects().delete()
        return True, 0
    else:
        obj = retrieve_object_by_identifier(data[0])
        if obj is None:
            print('No object with identifier \"' + data[0] + '\" found!')
            return False, 83
        obj.delete()
        if type(obj) == Person:
            nbdo = Crowd.objects()[0]
            nbdo.update(pull__persons=obj)
        elif type(obj) == Location:
            nbdo = Arena.objects()[0]
            nbdo.update(pull__locations=obj)
            rcobjects = Rcobject.objects(location=obj)
            for each in rcobjects:
                each.location = None
                each.save()
        elif type(obj) == Room:
            nbdo = Arena.objects()[0]
            nbdo.update(pull__rooms=obj)
            # TODO remove reference from doors and locations
        elif type(obj) == Door:
            nbdo = Arena.objects()[0]
            nbdo.update(pull__doors=obj)
        elif type(obj) == Rcobject:
            nbdo = Rcobjects.objects()[0]
            nbdo.update(pull__rcobjects=obj)
        return True, 0


def handle_remember(data):
    '''
    Hander for the data word remember. Will save a bdo to the knowledge base.
    :param data:
    :return:
    '''
    # data is list with one element. It is a xml format of a BDO class.
    # TODO: filter wrong querries
    xml_string = data[0]
    xml_tree = ET.fromstring(xml_string.encode('utf-8'))
    try:
        pass
    except Exception:
        print('XML parsing not successful.')
        return False, 91
    available_classes = {'persondata' : Person,
               'location' : Location,
               'room' : Room,
               'door' : Door,
               'rcobject' : Rcobject
               }
    if xml_tree.tag not in available_classes:
        print('Class \"' + xml_tree.tag + '\" is not a valid BDO class')
        return False, 92
    try:
        new_obj = available_classes[xml_tree.tag].from_xml(xml_tree)

        # check for old object with name and delete if possible
        old_obj = retrieve_object_by_identifier(new_obj.name)
        if old_obj is not None:
            print('There already was a ' + xml_tree.tag + ' with name "' + str(new_obj.name) + '", but it was overwritten.')
            if type(new_obj) == type(old_obj):
                # just update the object
                attribs_new = {x: new_obj.__getattribute__(x) for x in new_obj._fields}
                attribs_old = {x: old_obj.__getattribute__(x) for x in old_obj._fields}
                attribs_new.pop('id')
                modify_query = {}
                debug_print('New attribs: ' + str(attribs_new))
                debug_print('Old attribs: ' + str(attribs_old))
                bla = attribs_new['annotation'].viewpoints
                for attrib in attribs_new:
                    modify_query['set__' + attrib] = attribs_new[attrib]
                debug_print('query: ' + str(modify_query))
                old_obj.update(**modify_query)

                old_obj.reload()
                attribs_old = {x: old_obj.__getattribute__(x) for x in old_obj._fields}
                bla = attribs_old['annotation'].viewpoints

                return True, 0
            else:
                handle_forget([new_obj.name])

        new_obj.save()
        if type(new_obj) == Person:
            nbdo = Crowd.objects()[0]
            nbdo.update(add_to_set__persons=[new_obj])
        elif type(new_obj) == Location:
            nbdo = Arena.objects()[0]
            nbdo.update(add_to_set__locations=[new_obj])
        elif type(new_obj) == Room:
            nbdo = Arena.objects()[0]
            nbdo.update(add_to_set__rooms=[new_obj])
        elif type(new_obj) == Door:
            nbdo = Arena.objects()[0]
            nbdo.update(add_to_set__doors=[new_obj])
        elif type(new_obj) == Rcobject:
            nbdo = Rcobjects.objects()[0]
            nbdo.update(add_to_set__rcobjects=[new_obj])
        return True, 0
    except NoSuchLocationException:
        print('Could not find the location specified in BDO')
        return False, 94
    except NoSuchRoomException:
        print('Could not find the room specified in BDO')
        return False, 95
    except Exception:
        print('Error in converting the given xml to a BDO')
        print('Exact Exception: ' + str(traceback.format_exc()))
        return False, 93

