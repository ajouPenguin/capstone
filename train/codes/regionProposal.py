import selectiveSearch as ss
import gtcfeat as gtc
import numpy as np
import cv2
import multiprocessing as mp
from rectDetect import detectRect

def scoreComp(feat, dt, idx, retDic):
    score = gtc.getDistance(feat, dt)
    retDic[idx] = score

# extract feature(default filter is hog)
def extractFeature(img):
    return gtc.getFeat(img, algorithm='histogram')

# Perform selective search and return candidates
def processing(cv_img, db, opt='q'):
    rect = detectRect(cv_img)
    ret = []
    for x1, y1, x2, y2 in rect:
        score = []
        for _ in db:
            score.append(10000000000)
        cropped = cv_img[y1:y2, x1:x2]
        resized = cv2.resize(cropped, (50, 50))
        feat = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        feat = np.resize(feat, -1)
        if opt == 'f':
            feat = feat / 256
        minList = []
        cnt = 0
        for data in db:
            manager = mp.Manager()
            retDic = manager.dict()
            jobs = []
            idx = 0
            for datum in data:
                dt = datum['feat']
                if opt == 'f':
                    dt = dt / 256
                p = mp.Process(target=scoreComp, args=(feat, dt, idx, retDic))
                idx += 1
                jobs.append(p)
                p.start()
            for proc in jobs:
                proc.join()
            li = retDic.values()
            minList.append(min(li))
            cnt += 1

        score = min(minList)
        pred = minList.index(score)                
        ret.append((x1, x2, y1, y2, pred))
    return ret
