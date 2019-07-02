# generic imports
import sys
from knowledge_base.Classes import *
# XML imports
import xml.etree.ElementTree as ET
from xml.dom import minidom

# load annotation file. general stuff (argument handling etc)
args = sys.argv
if len(args) < 3:
    print('Usage: python map_annotation_tool_to_btl_converter.py <AnnotationFileMapAnnotationToolConform> <AnnotationFileBTLConform>')
    sys.exit()


inputstr = ''

with open(args[1], 'r') as f:
    inputstr = f.read()

annotations = []  # list where the xml annotations will be saved

# add those annotations to the list
annotationTree = ET.fromstring(inputstr)
for annotation in annotationTree.getchildren():
    if annotation.tag == 'ANNOTATION':
        annotations.append(annotation)

# define some methods to easier convert the changed btl classes to
def convert_point2d(point2d):
    '''
    Method to convert a point2d from old btl-xml to new btl-xml
    :param point2d: a ET.Element of a old btl-xml point2d
    :return: a  ET.Element of a new btl-xml point2d
    '''
    point = Point2d()
    point.x = float(point2d.get('x'))/1000
    point.y = float(point2d.get('y'))/1000
    return point.to_xml()


def convert_position_data(position_data):
    '''
    Method to convert a positionData from old btl-xml to new btl-xml. accepts a xml with basetag 'ROBOTPOSITION'
    :param position_data: a ET.Element of a old btl-xml positionData
    :return: a  ET.Element of a new btl-xml positionData
    '''
    posi_data = Positiondata()
    point2d = Point2d()
    for potential_posi in position_data.getchildren():
        if potential_posi.tag == 'POSITION':
            posi_data.theta = potential_posi.get('theta')
            point2d.x = potential_posi.get('x')
            point2d.y = potential_posi.get('y')
            posi_data.point2d = point2d
    return posi_data.to_xml()



def convert_viewpoint(viewpoint):
    '''
    Method to convert a viewpoint from old btl-xml to new btl-xml
    :param viewpoint: a ET.Element of a old btl-xml viewpoint
    :return: a  ET.Element of a new btl-xml viewpoint
    '''
    vp = Viewpoint()
    vp.label = viewpoint.get('label')
    for potential_roboposi in viewpoint.getchildren():
        if potential_roboposi.tag == 'ROBOTPOSITION':
            vp.positiondata = Positiondata.from_xml(convert_position_data(potential_roboposi))
    return vp.to_xml()

def convert_annotation(annotation):
    '''
    Method to convieniantly convert a annotation from old btl-xml to new btl-xml
    :param annotation: a ET.Element of a old btl-xml annotation
    :return: a  ET.Element of a new btl-xml annotation
    '''
    ano = Annotation()
    ano.label = annotation.get('label')
    print(ano.label)

    for child in annotation.getchildren():
        # may either be a generator, timestamp, precisepolygon or viewpoint
        # delete generators and timestamps
        if child.tag == 'GENERATOR' or child.tag == 'TIMESTAMP':
            annotation.remove(child)
        # convert viewpoints
        elif child.tag == 'VIEWPOINT':
            vp_new = convert_viewpoint(child)
            vp_new = Viewpoint.from_xml(vp_new)
            ano.viewpoints.append(vp_new)
        # convert point2d's in precisepolygons
        elif child.tag == 'PRECISEPOLYGON':
            ano.polygon = [[]]
            for potential_point in child.getchildren():
                if potential_point.tag == Point2d.get_tag():
                    poi_new = convert_point2d(potential_point)
                    poi_new = Point2d.from_xml(poi_new)
                    ano.polygon[0].append([poi_new.x, poi_new.y])
            ano.polygon[0].append(ano.polygon[0][0])
    return ano.to_xml()

root = ET.Element('LIST', attrib={'type': 'ANNOTATION'})
for anno in annotations:
    root.append(convert_annotation(anno))

write_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

with open(args[2], 'w') as f:
    f.write(str(write_string))