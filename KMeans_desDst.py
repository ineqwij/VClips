import numpy as np
import DstSIFT

def randCentre(dataset, k):
    centroid = []
    for i in range(0,k):
        # centre = np.random.randint(np.max(dataset), size=dataset[0].shape)
        centre = dataset[np.random.randint(0, len(dataset))]
        centroid.append(centre)
    return centroid

def reCentred(cent, dataset):
    if dataset == []:
        return cent
    sum = dataset[0]
    for i in range(1,len(dataset)):
        sum += dataset[i]
    centre = sum/len(dataset)
    return centre

def KMEANS(dataset, k):
    m = len(dataset)
    clusterChanged = True
    clusterAsses = np.mat(np.zeros([m,2]))
    centroids = randCentre(dataset, k)
    count = 0
    while clusterChanged:
        count += 1
        if count == 300:
            break
        clusterChanged = False
        for i in range(0, m):
            minDst = np.inf
            minIndex = -1
            for j in range(0, k):
                tempDst, _ = DstSIFT.getMatchesDis(dataset[i], centroids[j])
                if tempDst < minDst:
                    minDst = tempDst
                    minIndex = j
            if clusterAsses[i, 0] != minIndex:
                clusterChanged = True
            clusterAsses[i,:] = minIndex, minDst
        for i in range(0, k):
            elems = []
            for j in range(0,m):
                if clusterAsses[j,0] == i:
                    elems.append(dataset[j])
            centroids[i] = reCentred(centroids[i], elems)
    return centroids, clusterAsses
