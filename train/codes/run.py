import os
import gtcfeat as gtc
import numpy as np
import math
from brightChange import brightChange
from loadDBFromPath import loadDBFromPath
from outputVideo import outputVideo

def train(dataPath):

    db = []
    labels = []

    try:
        cnt = 0
        fileList = os.listdir(dataPath)
        if fileList == None:
            print('No file in path')
            return None
        for f in fileList:
            pa = os.path.join(dataPath, f)
            if not os.path.isdir(pa):
                continue
            db += [loadDBFromPath(pa, cnt)]
            cnt += 1
            labels.append(f)
    except Exception as e:
        print('No files in path')
        print(e)
        return None
    print(labels)
    outputVideo(db)

if __name__ == '__main__':
    train('../data')
