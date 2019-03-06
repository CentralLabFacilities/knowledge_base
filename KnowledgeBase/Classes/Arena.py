import mongoengine as me
from Room import Room
from Location import Location
from Door import Door
from Transmittable import Transmittable
import xml.etree.ElementTree as ET



class Arena(me.Document, Transmittable):
    locations = me.ListField(me.ReferenceField(Location))
    doors = me.ListField(me.ReferenceField(Door))
    rooms = me.ListField(me.ReferenceField(Room))

    def to_xml(self):
        root = ET.Element('ARENA')
        for loc in [x for x in self.locations if not x.ishidden]:
            root.append(loc.to_xml())
        for door in self.doors:
            root.append(door.to_xml())
        for room in self.rooms:
            root.append(room.to_xml())

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
        root = ET.Element('ARENA')
        for loc in [x for x in self.locations if not x.ishidden]:
            root.append(loc.to_xml_local())
        for door in self.doors:
            root.append(door.to_xml_local())
        for room in self.rooms:
            root.append(room.to_xml_local())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    def from_xml_local(cls, xml_tree):
        pass
