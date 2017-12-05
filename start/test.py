from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPixmap, QImage
import sys

import cv2

from py3_simulation.interface import RobotInterface
from py3_simulation.vision.token_locator import QrFinder
from time import time

'''
UP = 119
DOWN = 115
LEFT = 97
RIGHT = 100
DONE = 27
'''
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
DONE = 'E'

class Example(QWidget):

    def __init__(self):
        super().__init__()

        # GUI
        self.btn = None
        self.video_frame = None
        self.timer = None

        # Drone
        self.interface = None
        self.qrfinder = None
        self.qr_target = 0
        self.direction = 0

        self.v = 0

        self.default_task = [UP, UP, RIGHT, RIGHT, DOWN, LEFT, LEFT, DOWN, RIGHT, RIGHT, DONE]
        self.task = None

        #self.initDrone()
        self.initUI()

    def showVideo(self, cvImage):
        cv2.imwrite('%.04f.png' % time(), cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB))
        qimg = QImage(cvImage, cvImage.shape[1], cvImage.shape[0], cvImage.strides[0], QImage.Format_RGB888)
        self.video_frame.setPixmap(QPixmap.fromImage(qimg))

    def initDrone(self):
        self.task = self.default_task[:]

        self.interface = RobotInterface()
        self.qrfinder = QrFinder()

        self.qr_target = 1

        self.v = 0.025

        self.interface.set_target(0.5, 1.45, 0.2, 0)

    def initUI(self):
        self.timer = QBasicTimer()

        self.video_frame = QLabel(self)
        pixmap = QPixmap('capture0.png')
        self.video_frame.setPixmap(pixmap)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.setWindowTitle('Drone Test')
        self.resize(pixmap.width(),pixmap.height())
        self.show()

    def timerEvent(self, e):
        img = self.interface.get_image_from_camera()
        self.showVideo(img)

        value = self.qrfinder.find_code(img)
        try:
            x = value[0].data
            section, current, top, right, bottom, left = list(map(int, x.split(b'|')))
        except:
            section, current, top, right, bottom, left = 0, 0, 0, 0, 0, 0
            pass

        if self.qr_target == 0:
            print('[*] Illegal target')
            self.timer.stop()

        if self.qr_target == current:
            self.direction = 0

        if self.direction == 1:
            self.interface.move(0, 0, self.v, 0)
            return
        elif self.direction == 2:
            self.interface.move(0, -self.v, 0, 0)
            return
        elif self.direction == 3:
            self.interface.move(0, 0, -self.v, 0)
            return
        elif self.direction == 4:
            self.interface.move(0, self.v, 0, 0)
            return

        if self.direction == 0:
            ch, self.task = self.task[0], self.task[1:]

        print(section, current, top, right, left, bottom, ch)
        if ch == UP:
            self.qr_target = top
            self.direction = 1
        elif ch == RIGHT:
            self.qr_target = right
            self.direction = 2
        elif ch == DOWN:
            self.qr_target = bottom
            self.direction = 3
        elif ch == LEFT:
            self.qr_target = left
            self.direction = 4
        elif ch == DONE:
            self.doAction()

    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
            self.interface.stop()
        else:
            self.initDrone()
            self.timer.start(50, self)
            self.btn.setText('Stop')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
