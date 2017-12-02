import cv2
import numpy as np
import imutils
import os

def shapeDetect(c):
    shape = 'unidentified'
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 3:
        shape = 'triangle'
    elif len(approx) == 4:
        shape = 'rectangle'
    elif len(approx) == 5:
        shape = 'pentagon'
    else:
        shape = 'circle'

    return shape

def detectRect(im):
    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
    canny = cv2.Canny(gray_img, 0, 200)

    ret, thresh1 = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(canny, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(canny, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(canny, 127, 255, cv2.THRESH_TOZERO_INV)

    img_row1 = np.hstack([canny, thresh1, thresh2])
    img_row2 = np.hstack([thresh3, thresh4, thresh5])
    img_comb = np.vstack([img_row1, img_row2])

    thresh = thresh3

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    ret = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        shape = shapeDetect(c)
        c = c.astype('float')
        c = c.astype('int')
        x, y, w, h = cv2.boundingRect(c)
        if 50 < w < 100 and 50 < h < 100:
            ret.append([x,y,x+w,y+h])

    return ret
