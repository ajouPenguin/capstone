from regionProposal import processing
import cv2
import time

def outputVideo(db):
    # loading video
    outputColor = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    print('Load video')
    mpgFile = '../data/input.mpg'
    vidcap = cv2.VideoCapture(mpgFile)
    cnt = 0
    falseCnt = 0

    prevRect = []
    printed = []

    tic = time.time()

    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    print(length, width, height, fps)

    out = cv2.VideoWriter('../output/output.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (height, width))
    imCnt = 0
    while (True):
        spf = time.time()
        ret, image = vidcap.read()
        if ret == 0:
            out.release()
            break
        if (int(vidcap.get(1))):
            rect = processing(image, db)

            for (x1, x2, y1, y2, pred) in rect:
                try:
                    ec = outputColor[int(pred)]
                except:
                    ec = (255, 255, 255)
                lw = 1
                cv2.rectangle(image, (x1, y1), (x2, y2), ec, lw)

            cnt += 1
            out.write(image)
            print('%d frame' % (cnt))
            print('%s sec' % str(time.time()-spf))

    toc = time.time()
    print(toc - tic)
    return None
