from abc import ABC
from enum import Enum
import json
from anytree import NodeMixin


class ArchitectureLayers(Enum):
    root_syntactic_element = 'Root Syntactic Element'
    core_element = 'Core Element'
    kernel_element = 'Kernel Element'
    systems_element = 'Systems Element'


class Archtypes(Enum):
    element = 'element'
    relationship = 'relationship'
    sysml2_import = 'import'


class _RootSyntacticElement(ABC, NodeMixin):

    def __init__(self, name=None, parent=None,
                 sysml2_type=None,
                 idx=None,
                 uuid = None,
                 idx_parent=None, 
                 uuid_parent=None,
                 idx_related_element=None, 
                 related_element_name=None, 
                 value_types=None, 
                 constants=None, 
                 multiplicity=None, 
                 context_type=None, 
                 keywords=None, 
                 fully_qualified_name=None, 
                 fully_qualified_name_tagged=None, 
                 tree_level=None, 
                 element_text=None):
        
        """Base class for all syntactic elements, including Element and
        Relationship. Note that this class is not meant to be instantiated.
        """
        self.name = name
        self.parent = parent
        self.sysml2_type = sysml2_type
        self.idx = idx
        self.uuid = uuid
        self.idx_parent = idx_parent
        self.uuid_parent = uuid_parent
        self.idx_related_element = idx_related_element
        self.related_element_name = related_element_name
        self.value_types = value_types
        self.constants = constants
        self.multiplicity = multiplicity
        self.context_type = context_type
        self.keywords = keywords
        self.fully_qualified_name = fully_qualified_name
        self.fully_qualified_name_tagged = fully_qualified_name_tagged
        self.tree_level = tree_level
        self.element_text = element_text
        self.sysml2_layer = None # Set in child class definitions
        self.archtype = None
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    
    def to_dict(self):
        """Returns a dictionary representation of the object.
        Returns:
            _type_: _description_
        """
        dd = {}
        for k in ['sysml2_layer', 'archtype', 'sysml2_type', 'tree_level',
                  'name', 'idx', 'uuid', 'parent', 'idx_parent', 'uuid_parent',
                  'related_element_name', 'idx_related_element', 'multiplicity',
                  'value_types', 'constants', 'context_type', 'keywords', 
                  'fully_qualified_name', 'fully_qualified_name_tagged',
                  'element_text',]:
            if k == 'parent':
                dd[k] = getattr(self, '_NodeMixin__parent').name
            else:
                dd[k] = getattr(self, k)
        return dd


class Element(_RootSyntacticElement, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Element, self).__init__(name=name, parent=parent, **kwargs)
        self.archtype = Archtypes.element.value


class Relationship(_RootSyntacticElement, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Relationship, self).__init__(name=name, parent=parent, **kwargs)
        self.archtype = Archtypes.relationship.value


class Attribute(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Attribute, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value
        

class Comment(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Comment, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value
        

class Connection(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Connection, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value
        

class ConnectionEndPart(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(ConnectionEndPart, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class Doc(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Doc, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value


class Import(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Import, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value


class Item(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Item, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class Include(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Include, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class Objective(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Objective, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class Package(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Package, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.kernel_element.value
        

class Part(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Part, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value
        

class Port(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(Port, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class UseCase(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(UseCase, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value

        
        
class RelationshipConnect(Relationship, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(RelationshipConnect, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value

        
        
class RelationshipRedefines(Relationship, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(RelationshipRedefines, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value
        
        
class RelationshipSpecializes(Relationship, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):
        
        super(RelationshipSpecializes, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.root_syntactic_element.value


class RelationshipMessage(Relationship, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):

        super(RelationshipMessage, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class EnumDef(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):

        super(EnumDef, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value


class EnumValue(Element, NodeMixin):

    def __init__(self, name=None, parent=None, **kwargs):

        super(EnumValue, self).__init__(name=name, parent=parent, **kwargs)
        self.sysml2_layer = ArchitectureLayers.systems_element.value