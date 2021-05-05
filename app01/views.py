from typing import List, Any

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from app01.pojo import NeoGraph
from app01.utils import dealDict
from app01.nodes import *
from app01.relations import *

graph = NeoGraph("http://localhost:7474", username="neo4j", password="123456")


def searchAll(request):
    headNodeType = request.GET.get('headNodeType')
    headNode = request.GET.get('headNode')
    relationshipType = request.GET.get('relationshipType')
    tailNodeType = request.GET.get('tailNodeType')
    tailNode = request.GET.get('tailNode')
    returnResults = graph.search(headNodeType, dealDict(eval(headNode)), relationshipType,
                                 tailNodeType, dealDict(eval(tailNode)))
    if isinstance(returnResults, str):
        return HttpResponse('None')
    return JsonResponse(returnResults)


def showBridge(request):
    data = {'nodes': NeoGraph.nodesToJson(graph._searchNode(nodeType='bridge')), 'links': []}
    return setHeaders(JsonResponse(data))


def showRelations(request, identity: int, relationType: str):
    # data = {'nodes': NeoGraph.nodesToJson(graph.searchNode(nodeType='bridge')), 'links': []}
    # response = JsonResponse(data)
    # response = set(response)
    data = {'nodes': graph.searchRelationsByNodeAndRelationType(identity, relationType)[0],
            'links': graph.searchRelationsByNodeAndRelationType(identity, relationType)[1]}
    # print(data)
    return setHeaders(JsonResponse(data))


def deleteNodeAndLinks(request, identity):
    graph.deleteNodeAndLinks(identity)
    return HttpResponse('okkk')


def deleteRelationship(request, identity):
    graph.deleteRelationship(identity)
    return HttpResponse('okkkk')

def addRelationship(request):
    headNodeId = int(request.GET.get('headNodeId'))
    tailNodeId = int(request.GET.get('tailNodeId'))
    relationshipType = request.GET.get('relationshipAdd')
    graph.addRelationship(headNodeId, tailNodeId, relationshipType)
    return HttpResponse('okkkkk')

def setHeaders(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def addNode(request, nodeType):
    messages = eval(request.POST.get('message'))
    graph.addNote(nodeType, messages)
    return HttpResponse('ok')


def reviseNode(request, identity):
    messages = str(request.GET.get('message')).replace(' ', '').split(',')
    graph.reviseNode(identity, messages)
    return HttpResponse('ok')


def test(request):
    queryTitleList = str(request.GET.get('queryTitle')).replace(' ', '').split(',')
    data = {'nodes': NeoGraph.nodesToJson(graph.searchNode(nodeType=queryTitleList)), 'links': []}
    return setHeaders(JsonResponse(data))


def searchNode(request, name):
    # graph.searchBridgeNode(bridgeName=name)
    # print(name)
    return HttpResponse('hello')


def home(request):
    return render(request, 'home.html')


def index(request):
    return HttpResponse("这是主页")


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        return render(request, 'home.html')
