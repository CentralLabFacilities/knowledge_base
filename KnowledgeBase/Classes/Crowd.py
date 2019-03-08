import mongoengine as me
from Person import Person
from Transmittable import Transmittable
import xml.etree.ElementTree as ET


class Crowd(me.Document, Transmittable):
    persons = me.ListField(me.ReferenceField(Person))

    def to_xml(self):
        root = ET.Element('CROWD')
        for pers in self.persons:
            root.append(pers.to_xml())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    @classmethod
    def from_xml(cls, xml_tree):
        pass

    def to_xml_local(self):
        root = ET.Element('CROWD')
        for pers in self.persons:
            root.append(pers.to_xml_local())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    @classmethod
    def from_xml_local(cls, xml_tree):
        pass