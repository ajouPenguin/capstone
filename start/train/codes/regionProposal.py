import train.codes.gtcfeat as gtc
import numpy as np
import cv2
import multiprocessing as mp
from train.codes.rectDetect import detectRect

def scoreComp(feat, dt, idx, retDic):
    score = gtc.getDistance(feat, dt)
    retDic[idx] = score

# extract feature(default filter is hog)
def extractFeature(img):
    return gtc.getFeat(img, algorithm='hog')

# Perform selective search and return candidates
def processing(cv_img, clf, opt='q'):
    rect = detectRect(cv_img)
    ret = []
    for x1, y1, x2, y2 in rect:
        chk = 0
        for r in ret:
            (xx1, xx2, yy1, yy2, pp) = r
            if abs(xx1-x1) < 30 and abs(xx2 - x2) < 30 and abs(yy1 - y1) < 30 and abs(yy2 - y2) < 30:
                chk = 1
                break
            if x1 > xx1 and y1 > yy1 and x2 < xx2 and y2 < yy2:
                chk = 1
                break
            if x1 < xx2 and y1 < yy1 and x2 > xx2 and y2 > yy2:
                chk = 1
                break
        if chk == 1:
            continue
        score = []
        cropped = cv_img[y1:y2, x1:x2]
        resized = cv2.resize(cropped, (500, 500))
        feat = extractFeature(resized)
        feat = np.reshape(feat, (1, -1))
        pred = clf.predict(feat)
        ret.append((x1, x2, y1, y2, pred))
    return ret
