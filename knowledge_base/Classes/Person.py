import mongoengine as me
from Positiondata import Positiondata
from Transmittable import Transmittable
import xml.etree.ElementTree as ET


class Person(me.Document, Transmittable):
    age = me.StringField(max_length=10, default='')
    gender = me.StringField(max_length=50, default='')
    shirtcolor = me.StringField(max_length=50, default='')
    posture = me.StringField(max_length=50, default='')
    gesture = me.StringField(max_length=50, default='')

    position = me.EmbeddedDocumentField(Positiondata)
    name = me.StringField(max_length=100, default='')
    uuid = me.StringField(max_length=50, required=True, primary_key=True)
    faceid = me.IntField(default=-1)
    # pointcloud

    def to_xml(self):
        attribs = {x: self.__getattribute__(x) for x in self._fields}
        posi = attribs.pop('position')
        attribs = {x: str(attribs[x]) for x in attribs}

        root = ET.Element('PERSONDATA', attrib=attribs)
        root.append(posi.to_xml())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root


    @classmethod
    def from_xml(cls, xml_tree):
        pers = Person()
        pers.name = xml_tree.get('name')
        pers.uuid = xml_tree.get('uuid')
        pers.faceid = xml_tree.get('faceid')

        pers.gender = xml_tree.get('gender')
        pers.shirtcolor = xml_tree.get('shirtcolor')
        pers.posture = xml_tree.get('posture')
        pers.gesture = xml_tree.get('gesture')
        pers.age = xml_tree.get('age')

        print('DEBUG: got person ' + str(vars(pers)))
        print('DEBUG: got person(2) ' + str(pers._fields))

        for potential_posi in xml_tree.getchildren():
            if potential_posi.tag.lower() == Positiondata.get_tag().lower():
                pers.position = Positiondata.from_xml(potential_posi)
        return pers