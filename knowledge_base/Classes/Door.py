import mongoengine as me
from Room import Room
from Annotation import Annotation
from Transmittable import Transmittable
import xml.etree.ElementTree as ET


class Door(me.Document, Transmittable):
    roomone = me.ReferenceField(Room)
    roomtwo = me.ReferenceField(Room)
    annotation = me.EmbeddedDocumentField(Annotation)

    def to_xml(self):
        attribs = {x: self.__getattribute__(x) for x in self._fields}
        annot = attribs.pop('annotation')
        attribs.pop('id')
        root = ET.Element('DOOR', attrib={'roomone':attribs['roomone'].name, 'roomtwo':attribs['roomtwo'].name})
        root.append(annot.to_xml())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    @classmethod
    def from_xml(cls, xml_tree):
        pass
        # may throw no such room exception