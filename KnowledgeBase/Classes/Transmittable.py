from abc import abstractmethod


class Transmittable():

    @abstractmethod
    def to_xml(self):
        pass

    @classmethod
    def from_xml(cls, xml_tree):
        raise NotImplementedError

    @classmethod
    def from_xml_local(cls, xml_tree):
        return cls.from_xml(xml_tree)

    def to_xml_local(self):
        return self.to_xml()