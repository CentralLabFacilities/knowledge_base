import mongoengine as me
from Crowd import Crowd
from RCObjects import Rcobjects
from Arena import Arena
import xml.etree.ElementTree as ET


class Kbase(me.Document):
    identifier = me.StringField(max_length=50, unique=True)
    crowd = me.ReferenceField(Crowd)
    rcobjects = me.ReferenceField(Rcobjects)
    arena = me.ReferenceField(Arena)

    def to_xml(self):
        root = ET.Element('KBASE')
        root.append(self.crowd.to_xml())
        root.append(self.arena.to_xml())
        root.append(self.rcobjects.to_xml())

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root