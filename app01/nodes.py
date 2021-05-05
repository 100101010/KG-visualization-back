from time import sleep
from py2neo import Node


class baseNode(object):

    def __init__(self, identity: int, nodeType: str) -> None:
        super().__init__()
        self.id = identity
        self.nodeType = nodeType


class bridgeNode(baseNode):

    def __init__(self, bridgeNode: Node) -> None:
        super().__init__(bridgeNode.identity, str(bridgeNode.labels)[1:])
        self.bSpan = bridgeNode['bSpan']
        self.CSta = bridgeNode['CSta']
        self.bName = bridgeNode['bName']
        self.bCDate = bridgeNode['bCDate']
        self.bCen = bridgeNode['bCen']
        self.bRoad = bridgeNode['bRoad']
        self.bSCom = bridgeNode['bSCom']
        self.bWide = bridgeNode['bWide']
        self.bId = bridgeNode['bId']
        self.bLen = bridgeNode['bLen']
        self.bMUnit = bridgeNode['bMUnit']


class causeNode(baseNode):

    def __init__(self, causeNode: Node) -> None:
        super().__init__(causeNode.identity, str(causeNode.labels)[1:])
        self.cName = causeNode['cName']
        self.cDesc = causeNode['cDesc']
        self.cId = causeNode['cId']


class conclusionNode(baseNode):

    def __init__(self, conclusionNode: Node) -> None:
        super().__init__(conclusionNode.identity, str(conclusionNode.labels)[1:])
        self.bCId = conclusionNode['bCId']
        self.bCValue = conclusionNode['bCValue']
        self.bCName = conclusionNode['bCName']


class diseaseNode(baseNode):

    def __init__(self, diseaseNode: Node) -> None:
        super().__init__(diseaseNode.identity, str(diseaseNode.labels)[1:])
        self.bDId = diseaseNode['bDId']
        self.bDName = diseaseNode['bDName']


class fineStructureNode(baseNode):

    def __init__(self, fineStructureNode: Node) -> None:
        super().__init__(fineStructureNode.identity, str(fineStructureNode.labels)[1:])
        self.bsName = fineStructureNode['bsName']
        self.bsId = fineStructureNode['bsId']


class lastNode(baseNode):

    def __init__(self, lastNode: Node) -> None:
        super().__init__(lastNode.identity, str(lastNode.labels)[1:])
        self.name = lastNode['name']
        self.value = lastNode['value']
        self.lId = lastNode['lId']


class locationNode(baseNode):

    def __init__(self, locationNode: Node) -> None:
        super().__init__(locationNode.identity, str(locationNode.labels)[1:])
        self.bSLId = locationNode['bSLId']
        self.bSLName = locationNode['bSLName']


class structureNode(baseNode):

    def __init__(self, structureNode: Node) -> None:
        super().__init__(structureNode.identity, str(structureNode.labels)[1:])
        self.bSId = structureNode['bSId']
        self.bSMat = structureNode['bSMat']
        self.CNum = structureNode['CNum']
        self.bSName = structureNode['bSName']
        self.bSType = structureNode['bSType']


class technicalStateNode(baseNode):

    def __init__(self, technicalStateNode: Node) -> None:
        super().__init__(technicalStateNode.identity, str(technicalStateNode.labels)[1:])
        self.tName = technicalStateNode['tName']
        self.tValue = technicalStateNode['tValue']
        self.tId = technicalStateNode['tId']
        self.tBase = technicalStateNode['tBase']


class typeNode(baseNode):

    def __init__(self, typeNode: Node) -> None:
        super().__init__(typeNode.identity, str(typeNode.labels)[1:])
        self.bDTId = typeNode['bDTId']
        self.bDTName = typeNode['bDTName']


class autoSelectNode():

    def __init__(self, node1: Node) -> None:
        self.nodeDict = {
            'bridge': bridgeNode,
            'cause': causeNode,
            'conclusion': conclusionNode,
            'disease': diseaseNode,
            'fine_structure': fineStructureNode,
            'last': lastNode,
            'location': locationNode,
            'structure': structureNode,
            'technical_state': technicalStateNode,
            'type': typeNode
        }
        label = str(node1.labels)[1:]
        self.entity = self.nodeDict[label](node1)

    @property
    def node(self):
        return self.entity
