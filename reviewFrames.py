import cv2
import os
basePath = 'Videos/user'
basePathDir = 'Videos/images/user'
framePath = 'Frames/'
frame2Path = 'Frames_numC_5/'
clusterLog = open('clusterLog.txt', 'r')
cluster2Log = open('clusterLog2.txt', 'r')

def getSIFT(img, label, vID):
    outPath = framePath + label + '--' + vID.replace('.jpeg','') + '.jpg'
    print(outPath.replace('\n',''))
    cropped = img[150:1130, 0:720]
    gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    detector = cv2.xfeatures2d.SIFT_create(nfeatures=128)
    kps, des = detector.detectAndCompute(gray, None)
    imgKey = cv2.drawKeypoints(gray, kps, img)
    cv2.imwrite(outPath, imgKey)

def getV(tempStr):
    videoPath = basePath + tempStr[0] + '.mp4'
    videoCap = cv2.VideoCapture(videoPath)
    success, frame = videoCap.read()
    frameNum = 1
    while frameNum <= 25:
        success, frame = videoCap.read()
        frameNum += 1
    videoCap.release()
    getSIFT(frame, tempStr[1], tempStr[0])

def getF(tempStr):
    dirPath = basePathDir+tempStr[0]
    fPath = os.path.join(dirPath,'core-01.jpeg')
    print(fPath)
    IFrame = cv2.imread(fPath)
    getSIFT(IFrame, tempStr[1], tempStr[0])

def getFall(tempS):
    temp = tempS[0].split('_')
    # print(temp)
    dirPath = basePathDir + temp[0] + '_' + temp[1]
    fPath = os.path.join(dirPath,temp[2])
    frame = cv2.imread(fPath)
    getSIFT(frame, tempStr[1], tempStr[0])

for line in clusterLog.readlines():
    tempStr = line.replace(' ','').split(':')
    # print(tempStr)
    getF(tempStr)




