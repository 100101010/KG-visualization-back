import re

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, NodeMatch, RelationshipMatcher
from app01.nodes import *
from app01.relations import *
from app01.utils import *


class NeoGraph():

    def __init__(self, url: str, username: str, password: str) -> None:
        self.graphConnection = Graph(url, username=username, password=password)
        self.matcher = NodeMatcher(self.graphConnection)
        self.reMatcher = RelationshipMatcher(self.graphConnection)

    def addRelationship(self, headNodeId, tailNodeId, relatioshipType):
        headNode = self.searchNodeById(headNodeId)
        tailNode = self.searchNodeById(tailNodeId)
        rel = Relationship(headNode, relatioshipType, tailNode)
        self.graphConnection.merge(rel)

    def search(self, headNodeType, headNode, relationshipType, tailNodeType, tailNode):
        # 如果头节点为空
        data = {'nodes': [], 'links': []}
        flag = {'mutilHeadNodes': 0, 'mutilTailNodes': 0}
        if headNodeType == 'none':
            searchedHeadNode = None
        else:
            searchedHeadNodeResult = self.searchNode(headNodeType, headNode)
            if searchedHeadNodeResult.count() == 1:  # 表示头节点只有一个
                searchedHeadNode = searchedHeadNodeResult.first()
            elif searchedHeadNodeResult.count() == 0:
                return 'None'
            else:
                flag['mutilHeadNodes'] = 1

        if tailNodeType == 'none':
            searchedTailNode = None
        else:
            searchedTailNodeResult = self.searchNode(tailNodeType, tailNode)
            if searchedTailNodeResult.count() == 1:
                searchedTailNode = searchedTailNodeResult.first()
            elif searchedTailNodeResult.count() == 0:
                return 'None'
            else:
                flag['mutilTailNodes'] = 1

        if flag['mutilHeadNodes'] == 0 and flag['mutilTailNodes'] == 0:
            # 表明并没有头尾多节点的情况出现
            data = self._search(searchedHeadNode, searchedTailNode, relationshipType)
            return dealWithData(data)

        elif flag['mutilTailNodes'] == 0:
            # 如果头节点尾多个，尾节点要么为None，要么只有一个,变量searchedTailNode必被声明
            for tempHeadNode in searchedHeadNodeResult:
                resultData = self._search(tempHeadNode, searchedTailNode, relationshipType)
                for item in resultData['links']:
                    data['links'].append(item)
                for item in resultData['nodes']:
                    data['nodes'].append(item)
            return dealWithData(data)
        elif flag['mutilHeadNodes'] == 0:
            # 如果尾节点多个，头节点searchedHeadNode必已声明
            for tempTailNode in searchedTailNodeResult:
                resultData = self._search(searchedHeadNode, tempTailNode, relationshipType)
                for item in resultData['links']:
                    data['links'].append(item)
                for item in resultData['nodes']:
                    data['nodes'].append(item)
            return dealWithData(data)
        else:
            # 头尾节点都是多节点
            for tempHeadNode in searchedHeadNodeResult:
                for tempTailNode in searchedTailNodeResult:
                    resultData = self._search(tempHeadNode, tempTailNode, relationshipType)
                    for item in resultData['links']:
                        data['links'].append(item)
                    for item in resultData['nodes']:
                        data['nodes'].append(item)
            return dealWithData(data)

    def _search(self, searchedHeadNode, searchedTailNode, relationshipType):
        data = {'nodes': [], 'links': []}
        if relationshipType != 'none':
            for rel in self.reMatcher.match(nodes=(searchedHeadNode, searchedTailNode), r_type=relationshipType):
                data['nodes'].append(autoSelectNode(rel.start_node).node.__dict__)
                data['nodes'].append(autoSelectNode(rel.end_node).node.__dict__)
                data['links'].append(autoSelectRelationship(rel).__dict__)
        else:
            for rel in self.reMatcher.match(nodes=(searchedHeadNode, searchedTailNode)):
                data['nodes'].append(autoSelectNode(rel.start_node).node.__dict__)
                data['nodes'].append(autoSelectNode(rel.end_node).node.__dict__)
                data['links'].append(autoSelectRelationship(rel).__dict__)
        return data

    def addNote(self, nodeType: str, attrs: dict):
        tempNote = Node(nodeType, **attrs)
        self.graphConnection.create(tempNote)
        print("创建成功")

    def deleteRelationship(self, identity):
        deleteRelationship = self.reMatcher.get(identity)
        self.graphConnection.separate(deleteRelationship)

    def deleteNodeAndLinks(self, identity: int):
        deleteNode = self.matcher.get(identity)
        self.graphConnection.delete(deleteNode)

    def reviseNode(self, identity: int, message: list):
        tempNode = self.searchNodeById(identity)
        nodeType = str(tempNode.labels)[1:]
        if nodeType == 'bridge':
            properties = ['bSpan', 'CSta', 'bName', 'bCDate', 'bCen', 'bRoad', 'bSCom',
                          'bWide', 'bId', 'bLen', 'bMUnit']
        elif nodeType == 'cause':
            properties = ['cName', 'cDesc', 'cId']
        elif nodeType == 'conclusion':
            properties = ['bCId', 'bCValue', 'bCName']
        elif nodeType == 'disease':
            properties = ['bDId', 'bDName']
        elif nodeType == 'fine_structure':
            properties = ['bsName', 'bsId']
        elif nodeType == 'last':
            properties = ['name', 'value', 'lId']
        elif nodeType == 'location':
            properties = ['bSLId', 'bSLName']
        elif nodeType == 'structure':
            properties = ['bSId', 'bSMat', 'CNum', 'bSName', 'bSType']
        elif nodeType == 'technical_state':
            properties = ['tName', 'tValue', 'tId', 'tBase']
        else:
            properties = ['bDTId', 'bDTName']
        for index in range(len(properties)):
            if len(message[index]) != 0:
                tempNode[properties[index]] = message[index]
        self.graphConnection.push(tempNode)

    @staticmethod
    def nodesToJson(match):
        result = []
        index = 1
        if isinstance(match, NodeMatch):
            for node in match:
                result.append(autoSelectNode(node).node.__dict__)
                index += 1
                if index >= 25:
                    break
        elif isinstance(match, list):
            for matchObj in match:
                index = 1
                for node in matchObj:
                    result.append(autoSelectNode(node).node.__dict__)
                    index += 1
                    if index >= 25:
                        break
        return result

    def searchRelationsByNodeAndRelationType(self, identity: int, relationType: str):
        nodesResult = []
        linksResult = []
        bridgeNodeOne = self.matcher.get(identity)
        nodesResult.append(autoSelectNode(bridgeNodeOne).node.__dict__)
        for relationship in self.reMatcher.match(nodes=(bridgeNodeOne,), r_type=relationType):
            nodesResult.append(autoSelectNode(relationship.end_node).node.__dict__)
            linksResult.append(autoSelectRelationship(relationship).__dict__)

        return nodesResult, linksResult

    def searchNodeById(self, nodeIdentity: int):
        nodeMatchObj = self.matcher.get(nodeIdentity)
        if nodeMatchObj is None:
            raise ValueError('此节点ID不存在')
        else:
            return nodeMatchObj

    def _searchNode(self, nodeType, **kwargs):
        if isinstance(nodeType, str):
            return self.matcher.match(nodeType, **kwargs)
        elif isinstance(nodeType, list):
            nodeMatchList = []
            for type1 in nodeType:
                nodeMatchList.append(self.matcher.match(type1))
            return nodeMatchList

    def searchNode(self, nodeType, kwargs: dict):
        if isinstance(nodeType, str):
            return self.matcher.match(nodeType, **kwargs)
        elif isinstance(nodeType, list):
            nodeMatchList = []
            for type1 in nodeType:
                nodeMatchList.append(self.matcher.match(type1))
            return nodeMatchList
