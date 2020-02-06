import cv2
import numpy as np

def getSIFT(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    detector = cv2.xfeatures2d_SIFT.create()
    kp, des = detector.detectAndCompute(img,None)
    kp_img = cv2.drawKeypoints(gray,kp,None)
    return kp, des, kp_img

def getMatches(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    print(len(matches))
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good

def Halignment(img1, img2):
    kp1, des1, kp_img1 = getSIFT(img1)
    kp2, des2, kp_img2 = getSIFT(img2)
    matchPoints = getMatches(des1, des2)
    print(matchPoints[0].distance)
    imgOut = img1
    if len(matchPoints) >= 4:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in matchPoints]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in matchPoints]).reshape(-1, 1, 2)
        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 8)
        imgOut = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return imgOut

def Ptransform():
    return

img1 = cv2.imread('Videos/images/user1_5/core-01.jpeg')
img2 = cv2.imread('Videos/images/user1_10/core-01.jpeg')
resImg = Halignment(img1, img2)
allImg = np.concatenate((img1,img2,resImg),axis=1)
cv2.namedWindow('Result',cv2.WINDOW_NORMAL)
cv2.imshow('Result',allImg)
cv2.waitKey(5000)