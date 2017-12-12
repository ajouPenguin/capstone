import os
import train.codes.gtcfeat as gtc
import numpy as np
import math
from train.codes.brightChange import brightChange
from train.codes.loadDBFromPath import loadDBFromPath
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.externals import joblib
#from train.codes.outputVideo import outputVideo

def train(dataPath):

    db = []
    labels = []

    try:
        clf = joblib.load('./train/output/dump.pkl')
        print('Using trained model')
    except:

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
                print(pa)
                db += loadDBFromPath(pa, cnt)
                cnt += 1
                labels.append(f)
        except Exception as e:
            print('No files in path')
            print(e)
            return None

        clf = OneVsRestClassifier(LinearSVC(random_state=0))
        print('Building new model')
        print('Load data')

        # Make trainset and classes
        print('Make train set')
        trainset = np.float32([data['feat'] for data in db])
        classes = np.array([data['class'] for data in db])

        print(trainset)
        print(classes)

        # Start learning
        print('Start learning')
        clf.fit(trainset, classes)
    joblib.dump(clf, './train/output/dump.pkl')

    return clf
