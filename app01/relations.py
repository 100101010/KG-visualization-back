from py2neo import Graph, Node, Relationship

from app01.nodes import autoSelectNode


class autoSelectRelationship:

    def __init__(self, relationship: Relationship):
        self.source = autoSelectNode(relationship.start_node).node.id
        self.target = autoSelectNode(relationship.end_node).node.id
        self.relationshipId = relationship.identity
        self.relationship = list(relationship.types())[0]

