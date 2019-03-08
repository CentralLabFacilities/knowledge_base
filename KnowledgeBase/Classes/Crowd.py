import mongoengine as me
from Person import Person
import xml.etree.ElementTree as ET


class Crowd(me.Document):
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