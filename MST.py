import numpy as np
import DstSIFT
import os
import cv2
import desImg

clusterLog = open('clusterLog.txt', 'r')
basePathDir = 'Videos/images/user'
resSet = []
nodes = []
edges = []


def getSIFT(img):
    cropped = img[150:1130, 0:720]
    gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    detector = cv2.xfeatures2d.SIFT_create(nfeatures=128)
    kps, des = detector.detectAndCompute(gray, None)
    return des

def getF(tempStr):
    dirPath = basePathDir+tempStr[0]
    fPath = os.path.join(dirPath,'core-01.jpeg')
    print(fPath)
    IFrame = cv2.imread(fPath)
    descriptor = getSIFT(IFrame)
    node = desImg.Img(descriptor, tempStr[0], None)
    if tempStr[1] == "1":
        for i in nodes:
            preCostA_B = DstSIFT.getAvgDis(node.descriptor, i.descriptor)
            preCostB_A = DstSIFT.getAvgDis(i.descriptor, node.descriptor)
            edges.append(desImg.Edge(node.ImgID, i.ImgID, preCostA_B, [node.ImgID, i.ImgID], 0))
            edges.append(desImg.Edge(i.ImgID, node.ImgID, preCostB_A, [i.ImgID, node.ImgID], 0))
        nodes.append(node)
    edges.sort()

def findByID(imgID, nodeL):
    for n in nodeL:
        if imgID == n.ImgID:
            return n
    return None

def FindCircle(G, n, tar, nodeL):
    for e in G:
        if e.frm() == n.ImgID and e.to() == tar.ImgID:
            return [n], 1
        elif e.frm() == n.ImgID:
            temp = findByID(e.to(), nodeL)
            res, flag = FindCircle(G, temp, tar, nodeL)
            if flag == 0:
                continue
            elif flag == 1:
                res.append(n)
                return res, 1
    return [], 0

def getWtinG(G, toID):
    for e in G:
        if e.to() == toID:
            return e.wt()

def findInList(nameList, id):
    for name in nameList:
        if name.find(id) != -1:
            return name

def inCycle(nodeL, to, frm):
    for n in nodeL:
        if n.getSet() is not None:
            if to in n.getSet() and frm in n.getSet():
                return True
    return False

def dupRemv(l):
    r = []
    for i in l:
        if not i in r:
            r.append(i)
    return r

def treeDeduce():
    resGraph = []
    for i in range(1, len(nodes)):
        tempMin = edges[len(edges)-1]
        for e in edges:
            if e.frm() == nodes[0].ImgID:
                continue
            if nodes[i].ImgID == e.to():
                if e < tempMin:
                    tempMin = e
        resGraph.append(tempMin)
    resSet.append(resGraph)
    circleSet = []
    nameList = []
    newedges = []
    newnodes = []
    ifCirc = 0
    for i in range(1, len(nodes)):
        if nodes[i].visited:
            continue
        res, flag = FindCircle(resGraph, nodes[i], nodes[i], nodes)
        if flag == 1:
            ifCirc = 1
            str = ""
            tempList = []
            for id in res:
                id.visit()
                str += "||" + id.ImgID
                circleSet.append(id.ImgID)
                tempList.append(id.ImgID)
            nameList.append(str)
            newnodes.append(desImg.Img(0, str, tempList))
        elif flag == 0:
            nodes[i].visit()
            newnodes.append(nodes[i])
    for e in edges:
        if e.frm() in circleSet and e.to() in circleSet:
            if inCycle(newnodes, e.to(), e.frm()):
                continue
            else:
                str1 = findInList(nameList, e.frm())
                str2 = findInList(nameList, e.to())
                newedges.append(desImg.Edge(str1, str2, e.wt() - getWtinG(resGraph, e.to()), [e.frm(),e.to()], 3))

        elif e.frm() in circleSet and e.to() not in circleSet:
            str = findInList(nameList, e.frm())
            newedges.append(desImg.Edge(str, e.to(), e.wt(), [e.frm(), e.to()], 2))
        elif e.frm() not in circleSet and e.to() in circleSet:
            str = findInList(nameList, e.to())
            newedges.append(desImg.Edge(e.frm(), str, e.wt() - getWtinG(resGraph, e.to()), [e.frm(), e.to()], 1))
        elif e.frm() not in circleSet and e.to() not in circleSet:
            newedges.append(e)
    print(len(newedges))
    preRes = resGraph
    while ifCirc == 1:
        resGraph = []
        tempnewedges = newedges
        tempnewnodes = newnodes
        for i in range(0, len(tempnewnodes)):
            tempMin = tempnewedges[len(tempnewedges) - 1]
            for e in tempnewedges:
                if tempnewnodes[i].ImgID == e.to():
                    if e < tempMin:
                        tempMin = e
            resGraph.append(tempMin)
        resSet.append(resGraph)
        for n in tempnewnodes:
            print(n.ImgID)
        print("----------")
        for e in resGraph:
            c, f = e.defold()
            print("from:", e.frm(), "//to:", e.to(), "//wt:", e.wt(), "//from-to: ", c, "//flag:", f)
        print("----------")
        circleSet = []
        nameList = []
        newedges = []
        newnodes = []
        ifCirc = 0
        for n in tempnewnodes:
            n.devis()
        for i in range(0, len(tempnewnodes)):
            if tempnewnodes[i].visited:
                continue
            res, flag = FindCircle(resGraph, tempnewnodes[i], tempnewnodes[i], tempnewnodes)
            if flag == 1:
                ifCirc = 1
                str = ""
                tempList = []
                for id in res:
                    id.visit()
                    str += "||" + id.ImgID
                    circleSet.append(id.ImgID)
                    tempList.append(id.ImgID)
                str = str.replace("||||", '||')
                nameList.append(str)
                newnodes.append(desImg.Img(0, str, tempList))
            elif flag == 0:
                tempnewnodes[i].visit()
                newnodes.append(tempnewnodes[i])
        for e in tempnewedges:
            if e.frm() in circleSet and e.to() in circleSet:
                if inCycle(newnodes, e.to(), e.frm()):
                    continue
                else:
                    str1 = findInList(nameList, e.frm())
                    str2 = findInList(nameList, e.to())
                    c, f = e.defold()
                    newedges.append(desImg.Edge(str1, str2, e.wt() - getWtinG(resGraph, e.to()), [c[0], c[1]], 3))
            elif e.frm() in circleSet and e.to() not in circleSet:
                str = findInList(nameList, e.frm())
                c, f = e.defold()
                if "||" in e.to():
                    newedges.append(desImg.Edge(str, e.to(), e.wt(), [c[0], c[1]], 2))
                else:
                    newedges.append(desImg.Edge(str, e.to(), e.wt(), [c[0], e.to()], 2))
            elif e.frm() not in circleSet and e.to() in circleSet:
                str = findInList(nameList, e.to())
                c, f = e.defold()
                if "||" in e.frm():
                    newedges.append(desImg.Edge(e.frm(), str, e.wt() - getWtinG(resGraph, e.to()), [c[0], c[1]], 1))
                else:
                    newedges.append(desImg.Edge(e.frm(), str, e.wt() - getWtinG(resGraph, e.to()), [e.frm(), c[1]], 1))
            elif e.frm() not in circleSet and e.to() not in circleSet:
                newedges.append(e)
    resNodes = []
    resGraph = []
    ite = len(resSet)-1
    while ite >= 0:
        g = resSet[ite]
        for e in g:
            c, f = e.defold()
            if f == 0:
                if not c[1] in resNodes:
                    resNodes.append(c[1])
                    resGraph.append(c)
            elif f == 1:
                b = 0
                for id in resNodes:
                    if id in e.to():
                        b = 1
                        break
                if b == 1:
                    # print(resNodes)
                    # print("from:", e.frm(), "//to:", e.to(), "//wt:", e.wt(), "//from-to: ", c, "//flag:", f)
                    continue
                if not c[1] in resNodes:
                    resNodes.append(c[1])
                    resGraph.append(c)
            elif f == 2:
                b = 0
                for id in resNodes:
                    if id in e.to():
                        b = 1
                        break
                if b == 1:
                    # print("from:", e.frm(), "//to:", e.to(), "//wt:", e.wt(), "//from-to: ", c, "//flag:", f)
                    continue
                if not c[1] in resNodes:
                    resNodes.append(c[1])
                    resGraph.append(c)
        ite -= 1
    return resNodes, resGraph

for line in clusterLog.readlines():
    tempStr = line.replace(' ','').replace('\n','').split(':')
    # print(tempStr)
    getF(tempStr)
n, e = treeDeduce()
print("----------")
for i in e:
    print("from: ", i[0], " || to: ", i[1])

