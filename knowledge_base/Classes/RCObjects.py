import mongoengine as me
from RCObject import Rcobject
from Transmittable import Transmittable
import xml.etree.ElementTree as ET


class Rcobjects(me.Document, Transmittable):
    rcobjects = me.ListField(me.ReferenceField(Rcobject))

    def to_xml(self):
        root = ET.Element('RCOBJECTS')
        for ob in self.rcobjects:
            root.append(ob.to_xml())

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
        root = ET.Element('RCOBJECTS')
        for ob in self.rcobjects:
            root.append(ob.to_xml_local())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    @classmethod
    def from_xml_local(cls, xml_tree):
        pass