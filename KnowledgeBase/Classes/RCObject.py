import mongoengine as me
from Location import Location
import xml.etree.ElementTree as ET


class Rcobject(me.Document):
    name = me.StringField(max_length=50, unique=True, default='')
    location = me.ReferenceField(Location)
    category = me.StringField(max_length=50, default='')
    shape = me.StringField(max_length=50, default='')
    color = me.StringField(max_length=50, default='')
    type = me.StringField(max_length=50, default='')
    size = me.IntField(default=0)
    weight = me.IntField(default=0)

    def to_xml(self):
        attribs = {x: self.__getattribute__(x) for x in self._fields}
        location = attribs.pop('location')
        if location is not None:
            attribs['room'] = location.room.name
            attribs['location'] = location.name
        else:
            attribs['room'] = ''
            attribs['location'] = ''
        attribs['graspdifficulty'] = '0'
        attribs.pop('id')
        attribs = {x: str(attribs[x]) for x in attribs}
        root = ET.Element('RCOBJECT', attrib=attribs)

        gen = ET.SubElement(root, 'GENERATOR')
        gen.text = 'Kbase'
        time = ET.SubElement(root, 'TIMESTAMP')
        inserted = ET.SubElement(time, 'INSERTED', {'value': '1'})
        updated = ET.SubElement(time, 'UPDATED', {'value': '1'})
        return root

    @classmethod
    def from_xml(cls):
        pass
        # may throw no such location exception
