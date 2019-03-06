from abc import abstractmethod, ABC


class Transmittable(ABC):

    @abstractmethod
    def to_xml(self):
        pass

    @abstractmethod
    @classmethod
    def from_xml(cls, xml_tree):
        pass

    @classmethod
    def from_xml_local(cls, xml_tree):
        return cls.from_xml(xml_tree)

    def to_xml_local(self):
        return self.to_xml()