import os
import cv2
import numpy as np
from train.codes.regionProposal import extractFeature
from train.codes.brightChange import brightChange

# Loads database images
def loadDBFromPath(path, classnum, isFiltered=0):
    db = []
    for file in os.listdir(path):
        if not file.upper().endswith('.JPG'):
            continue
        data = {}
        data['class'] = classnum
        img = cv2.imread(path + '/' + file, cv2.IMREAD_COLOR)
        resized = cv2.resize(img, (50, 50))
        if isFiltered :
            data['feat'] = extractFeature(img)
        else :
            data['feat'] = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            data['feat'] = np.resize(data['feat'], -1)
        db.append(data)

    return db
