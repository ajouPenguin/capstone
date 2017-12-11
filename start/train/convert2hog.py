import cv2
import os
from skimage.feature import hog

li1 = os.listdir('./type1/')
li2 = os.listdir('./type2/')
li3 = os.listdir('./type3/')
li4 = os.listdir('./QR/')

im1 = []
im2 = []
im3 = []
im4 = []

for l in li1:
    im = cv2.imread('./type1/'+l)
    im1.append(im)

for l in li2:
    im = cv2.imread('./type2/'+l)
    im2.append(im)

for l in li3:
    im = cv2.imread('./type3/'+l)
    im3.append(im)

for l in li4:
    im = cv2.imread('./QR/'+l)
    im4.append(im)

for i in range(len(im1)):
    im = cv2.cvtColor(im1[i], cv2.COLOR_RGB2GRAY)
    img = cv2.resize(im, dsize=(320, 320), interpolation=cv2.INTER_CUBIC)
    fn = li1[i]

    fd, hog_img = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
    hog_img *= 255
    cv2.imwrite('./new/' + fn, hog_img)


for i in range(len(im2)):
    im = cv2.cvtColor(im2[i], cv2.COLOR_RGB2GRAY)
    img = cv2.resize(im, dsize=(320, 320), interpolation=cv2.INTER_CUBIC)
    fn = li2[i]

    fd, hog_img = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
    hog_img *= 255
    cv2.imwrite('./new/' + fn, hog_img)



for i in range(len(im3)):
    im = cv2.cvtColor(im3[i], cv2.COLOR_RGB2GRAY)
    img = cv2.resize(im, dsize=(320, 320), interpolation=cv2.INTER_CUBIC)
    fn = li3[i]

    fd, hog_img = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
    hog_img *= 255
    cv2.imwrite('./new/' + fn, hog_img)


for i in range(len(im4)):
    im = cv2.cvtColor(im4[i], cv2.COLOR_RGB2GRAY)
    img = cv2.resize(im, dsize=(320, 320), interpolation=cv2.INTER_CUBIC)
    fn = li4[i]

    fd, hog_img = hog(img, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
    hog_img *= 255
    cv2.imwrite('./new/' + fn, hog_img)
