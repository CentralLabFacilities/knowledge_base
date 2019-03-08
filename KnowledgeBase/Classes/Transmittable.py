from abc import abstractmethod, ABCMeta


class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


class Transmittable():

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_xml(self):
        pass

    @abstractclassmethod
    def from_xml(cls, xml_tree):
        pass

    @classmethod
    def from_xml_local(cls, xml_tree):
        return cls.from_xml(xml_tree)

    def to_xml_local(self):
        return self.to_xml()