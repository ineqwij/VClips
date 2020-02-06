import numpy as np
import cv2

alpha = 1

def getScdClosest(disSet, closest):
    loc = int(np.argmax(disSet))
    ret = disSet[loc]
    for i in range(0, len(disSet)):
        if i == closest:
            continue
        if float(disSet[i]) < float(ret):
            ret = disSet[i]
            loc = i
    return ret, loc

def matchPoints(desSet1, des2):
    disSet = []
    for i in range(0,len(desSet1)):
        dis = desDistance(desSet1[i], des2)
        disSet.append(dis)
    closest = int(np.argmin(disSet))
    dis_scdClosest, scdClosest = getScdClosest(disSet, closest)
    dis_closest = disSet[closest]
    if dis_closest < alpha*dis_scdClosest:
        return 1, closest, dis_closest
    else:
        return 0, None, None

def desDistance(des1, des2):
    norm = np.linalg.norm((des2-des1), ord=2)
    distance = norm/len(des2)
    return distance

def getAvgDis(imgDes1, imgDes2):
    desMatched = []
    sum = 0
    for descriptor in imgDes2:
        flag, clos, dis_clos = matchPoints(imgDes1, descriptor)
        if flag == 1:
            desMatched.append(dis_clos)
            sum += dis_clos
    ret = sum/len(desMatched)
    return ret

def getMatchesDis(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)
    sum = 0
    for m in matches:
        sum += m.distance
    ret = sum/len(matches)
    return ret, matches