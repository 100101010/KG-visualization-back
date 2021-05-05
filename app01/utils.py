def dealDict(tempDict:dict):
    newDict = {}
    for k in tempDict:
        if isinstance(tempDict[str(k)], int) or len(str(tempDict[str(k)])) != 0:
            newDict[str(k)] = tempDict[str(k)]
    return newDict


def dealRepeatDict(data, key):
    newData = [] #  用来存放去重后的字典列表
    values = [] # 用来存放当前已有的值
    for dic in data:
        if dic[key] not in values:
            values.append(dic[key])
            newData.append(dic)
    return newData

def dealWithData(data):
    data['nodes'] = dealRepeatDict(data['nodes'], 'id')
    data['links'] = dealRepeatDict(data['links'], 'relationshipId')
    return data