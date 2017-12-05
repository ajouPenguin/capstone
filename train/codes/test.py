import cv2
import os
import sys

import skvideo.io

if len(sys.argv) < 2:
	print('ARGS')
	exit(1)

mpgFile = sys.argv[1] #'/home/hyeon/input.mpg'

print(mpgFile)

assert(os.access(mpgFile, os.F_OK) == True)

with open(mpgFile, 'rb') as f:
	print (repr(f.read(4)))

vidcap = cv2.VideoCapture(mpgFile)
#vidcap = skvideo.io.VideoCapture(mpgFile.encode('utf-8'))
assert(vidcap.isOpened() == True)

length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vidcap.get(cv2.CAP_PROP_FPS)

print (length, width, height, fps)



