import cv2

mpgFile = '../data/input.mpg'

vidcap = cv2.VideoCapture(mpgFile)

length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = vidcap.get(cv2.CAP_PROP_FPS)

print (length, width, height, fps)



