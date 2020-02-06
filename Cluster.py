import cv2
from sklearn.cluster import KMeans
import os
import numpy as np
import KMeans_desDst
import matplotlib.pyplot as plt
import desImg

keyFrames = []
data = []
videoNum = []
Descriptors = []
basePath = 'Videos/'
basePathIFrame = 'Videos/images/user'

def getSIFT(img):
    cropped = img[150:1130, 0:720]
    gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    detector = cv2.xfeatures2d.SIFT_create()
    kps, des = detector.detectAndCompute(gray, None)
    if des is None:
        return None
    '''
    cv2.imshow('windows', cropped)
    cv2.waitKey(1500)
    imKey = cv2.drawKeypoints(cropped,kps,cropped)
    cv2.imshow('windows', imKey)
    cv2.waitKey(2000)
    '''
    # print(des[0])
    if len(des) < 200:
        return None
    des = des[0:200]
    return des

def procFrame(videoPath):
    videoCap = cv2.VideoCapture(videoPath)
    success, frame = videoCap.read()
    frameNum = 1
    tempDes = getSIFT(frame)
    while len(tempDes) < 63:
        if frameNum <= 25:
            continue
        success, frame = videoCap.read()
        frameNum += 1
        tempDes = getSIFT(frame)
    videoCap.release()
    return frame, tempDes.flatten(), tempDes

def procIFrames(dirPath):
    filename = os.path.join(dirPath, 'core-01.jpeg')
    IFrame = cv2.imread(filename)
    tempDes  = getSIFT(IFrame)
    return IFrame, tempDes

def getFromFrames():
    countVideo = 0
    for i in range(1, 6):
        for j in range(1, 11):
            tempStr = str(i) + '_' + str(j)
            dirPath = basePathIFrame + tempStr
            print(dirPath)
            frame, SIFTDes = procIFrames(dirPath)
            data.append(SIFTDes.flatten())
            Descriptors.append(SIFTDes)
            keyFrames.append(frame)
            videoNum.append(tempStr)
            countVideo += 1
    return countVideo

def getFromVideo():
    countVideo = 0
    for i in range(1,6):
        #if i == 3:
        #    continue
        for j in range(1,21):
            tempStr = str(i) + '_' + str(j)
            videoPath = basePath + tempStr + '.mp4'
            print(videoPath)
            frame, SIFTDes,descriptor = procFrame(videoPath)
            keyFrames.append(frame)
            data.append(SIFTDes)
            Descriptors.append(descriptor)
            videoNum.append(tempStr)
            countVideo += 1
    return countVideo

def getAllFrames():
    countFrames = 0
    for i in range(1, 2):
        for j in range(1, 11):
            tempStr = str(i) + '_' + str(j)
            dirPath = basePathIFrame + tempStr
            for files in os.listdir(dirPath):
                tempStrF = tempStr + '_' + files
                filename = os.path.join(dirPath, files)
                print(filename)
                IFrame = cv2.imread(filename)
                if IFrame is None:
                    continue
                tempDes = getSIFT(IFrame)
                if tempDes is None:
                    continue
                else:
                    data.append(tempDes.flatten())
                    Descriptors.append(tempDes)
                    keyFrames.append(IFrame)
                    videoNum.append(tempStrF)
                countFrames += 1
    return countFrames

numV = getFromFrames()

distortion = []
for k in range(2,12):
    estimator = KMeans(n_clusters=k, max_iter=500)
    estimator.fit(data)
    distortion.append(estimator.inertia_)
plt.plot(range(2,12), distortion,'bo-', mfc='r')
plt.show()

prev = distortion[0] - distortion[1]
diff = distortion[1] - distortion[2]
x = prev - diff
resK = 3
for i in range(3,10):
    # print(str(resK))
    # print(x)
    diff = distortion[i-1] - distortion[i]
    prev = distortion[i-2] - distortion[i-1]
    if prev - diff > x:
        x = prev - diff
        resK = i+1

KM = KMeans(n_clusters=resK, max_iter=500)
KM.fit(data)

'''
c, estimator_desDst = KMeans_desDst.KMEANS(Descriptors, 4)
print(estimator_desDst)
'''

for i in range(0,numV):
    outStr = videoNum[i] + ': ' + str(KM.labels_[i]+1)
    print(outStr)
print(KM.labels_)

