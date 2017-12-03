import os
import cv2

fl = os.listdir('./')
cnt = 0
for f in fl:
    if f != cnt:
        if f == 'changeName.py':
            continue
        img = cv2.imread(f)
        cv2.imwrite(str(cnt) + '.jpg', img)
        os.remove(f)
        cnt += 1