from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QBasicTimer
from OpenGL.GL import *
import cv2
from math import *
import time
import multiprocessing as mp
import threading
import os
import squareSection as ss
from py3_simulation import control
from py3_simulation.interface import RobotInterface
from py3_simulation.vision.token_locator import QrFinder
from train.codes.regionProposal import extractFeature
from train.codes.rectDetect import detectRect
from train.codes.run import train
import numpy as np

UP = 119
DOWN = 115
LEFT = 97
RIGHT = 100
DONE = 27
outputColor = [(0, 0 , 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
clf = train('./train/data')

mainwindow_class = uic.loadUiType("title.ui")[0]
quitbox_class = uic.loadUiType("quitbox.ui")[0]
learningbox_class = uic.loadUiType("learningbox.ui")[0]
drone_label_count = 2   #드론라벨카운트 2부터 +1씩
threshold = 80

class quitBox(QWidget, quitbox_class):
    def __init__(self, parent):
        super(quitBox, self).__init__(parent)
        self.setGeometry(550, 300, 300, 100)
        self.setupUi(self)
    def accept(self):
        exit()
    def reject(self):
        self.parent().btn_enable()
        self.close()

class learningBox(QWidget, learningbox_class):
    def __init__(self, parent):
        super(learningBox, self).__init__(parent)
        self.setGeometry(430, 200, 421, 281)
        self.setupUi(self)
        self.timer = QBasicTimer()
        self.i = 0

    def timerEvent(self, e):
        if self.i >= 100:
            self.timer.stop()
            return

        self.i += 1
        self.learningBar.setValue(self.i)

    def finish_learning(self):
        self.parent().btn_enable()
        self.close()

    def start(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def cancel(self):
        self.learningBar.setValue(0)
        self.parent().btn_enable()
        self.close()
        
class DronePath(QWidget, pathbox_class):
    def __init__(self, parent):
        super(DronePath, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(450, 150, 341, 451)
        self.initTable()
        self.cur = 1
        self.row = 3
        self.height = 3
        self.moves = []
        self.text = ""

    def initTable(self):
        self.initTable2(self.section1)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEditable)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/controlBtn/controlbtn/start.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.section1.setItem(1, 1, item)
        self.initTable2(self.section2)
        self.initTable2(self.section3)
        self.initTable2(self.section4)
        self.initTable2(self.section5)
        self.initTable2(self.section6)
        self.initTable2(self.section7)
        self.initTable2(self.section8)
        self.initTable2(self.section9)
    def initTable2(self, section):
        i, j = 0, 0
        width = section.width() / section.columnCount() - 1
        height = section.height() / section.rowCount() - 1
        while i < self.section1.columnCount():
            section.setColumnWidth(i, width)
            i += 1
        while j < self.section1.rowCount():
            section.setRowHeight(j, height)

            j += 1
        section.setIconSize(QtCore.QSize(23, 23))

    def doUp(self):
        next = self.cur + self.row
        if((self.cur / self.row) <= (self.height - 1)):
            section = self.getcurSection(self.cur)
            self.setRec(section, 0, 1)
            section = self.getcurSection(next)
            self.setRec(section, 2, 1)
            self.setTri(section, 1, 1)
            self.cur = next
            self.moves.append(UP)
            self.text += "UP "
            self.textEdit.setText(self.text)
    def doDown(self):
        next = self.cur - self.row
        if((self.cur / self.row) > 1):
            section = self.getcurSection(self.cur)
            self.setRec(section, 2, 1)
            section = self.getcurSection(next)
            self.setRec(section, 0, 1)
            self.setTri(section, 1, 1)
            self.cur = next
            self.moves.append(DOWN)
            self.text += "DOWN "
            self.textEdit.setText(self.text)
    def doLeft(self):
        next = self.cur - 1
        if ((self.cur % self.row) != 1):
            section = self.getcurSection(self.cur)
            self.setRec(section, 1, 0)
            section = self.getcurSection(next)
            self.setRec(section, 1, 2)
            self.setTri(section, 1, 1)
            self.cur = next
            self.moves.append(LEFT)
            self.text += "LEFT "
            self.textEdit.setText(self.text)
    def doRight(self):
        next = self.cur + 1
        if ((self.cur % self.row) != 0):
            section = self.getcurSection(self.cur)
            self.setRec(section, 1, 2)
            section = self.getcurSection(next)
            self.setRec(section, 1, 0)
            self.setTri(section, 1, 1)
            self.cur = next
            self.moves.append(RIGHT)
            self.text += "RIGHT "
            self.textEdit.setText(self.text)
    def doRewind(self):
        self.parent().drone_path()
        self.close()

    def doFinish(self):
        self.parent().btn_enable()
        self.moves.append('DONE')
        test_moves = self.moves[:]
        self.close()

    def getcurSection(self, cur):
        if(cur == 1): return self.section1
        elif(cur == 2): return self.section2
        elif(cur == 3): return self.section3
        elif(cur == 4): return self.section4
        elif(cur == 5): return self.section5
        elif(cur == 6): return self.section6
        elif(cur == 7): return self.section7
        elif(cur == 8): return self.section8
        elif(cur == 9): return self.section9

    def setRec(self, section, x, y):
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(42, 122, 138))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEditable)
        section.setItem(x, y, item)
    def setTri(self, section, x, y):
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(42, 122, 138))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEditable)
        section.setItem(x, y, item)

class DroneControl(QWidget):
    def __init__(self, show):
        super().__init__()

        self.showFunc = show
        self.outputVideo = cv2.VideoWriter('./train/output/output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (512, 512))
        self.interface = None
        self.qrfinder = None
        self.qr_target = 0
        self.direction = 0
        self.sections = ss.sectionList()
        self.prevRects = []
        self.prevDirection = 0
        self.detected = [0, 0, 0, 0]

        self.v = 0

        self.default_task = [RIGHT, RIGHT, UP, UP, LEFT, LEFT, DOWN, RIGHT, RIGHT, DOWN, LEFT, LEFT, DONE]#[UP, UP, RIGHT, RIGHT, DOWN, LEFT, LEFT, DOWN, RIGHT, RIGHT, LEFT, LEFT, DONE]
        self.task = None

        self.timer = QBasicTimer()

    def timerEvent(self, e):
        img = self.interface.get_image_from_camera()
        value = self.qrfinder.find_code(img)

        try:
            x = value[0].data
            section, current, top, right, bottom, left = list(map(int, x.split(b'|')))
        except:
            section, current, top, right, bottom, left = 0, 0, 0, 0, 0, 0
            pass

        cimg = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)
        if (self.direction == 2 or self.direction == 4) and (current == 0):
            rects = detectRect(cimg)
            for (x1, y1, x2, y2) in rects:
                check = 0
            # 이전 프레임에서 찾아서 더했던 barcode label 걸러내기
                if len(self.prevRects) > 0:
                    for i in range(len(self.prevRects)):
                        (xx1, yy1, xx2, yy2, cnt, pp) = self.prevRects[i]
                        if abs(x1 - xx1) < threshold and abs(x2 - xx2) < threshold and abs(y1 - yy1) < threshold and abs(y2 - yy2) < threshold:
                            self.prevRects[i] = (x1, y1, x2, y2, -1, pp)
                            pred = pp
                            check = 1
                            break
                    if check == 0:
                        for i in range(len(self.prevRects)):
                            (xx1, yy1, xx2, yy2, cnt, pp) = self.prevRects[i]
                            if xx1 - 80 < x1 < xx2 + 80 and xx1 - 80 < x2 < xx2 + 80 and yy1 - 80 < y1 < yy2 + 80 and yy1 - 80 < y2 < yy2 + 80:
                                x1, y1, y2, y2 = xx1, yy1, xx2, yy2
                                pred = pp
                                check = 1
                                break
                    if check == 0:
                        cropped = cimg[y1:y2, x1:x2]
                        resized = cv2.resize(cropped, (500, 500))
                        feat = extractFeature(resized)
                        feat = np.reshape(feat, (1, -1))
                        pred = clf.predict(feat)
                        self.detected[pred] += 1
                        self.prevRects.append((x1, y1, x2, y2, -1, pred))
                else:
                    cropped = cimg[y1:y2, x1:x2]
                    resized = cv2.resize(cropped, (500, 500))
                    feat = extractFeature(resized)
                    feat = np.reshape(feat, (1, -1))
                    pred = clf.predict(feat)
                    self.detected[pred] += 1
                    self.prevRects.append((x1, y1, x2, y2, -1, pred))
                try:
                    ec = outputColor[int(pred)]
                except:
                    ec = (255, 255, 255)
                lw = 1
                cv2.rectangle(cimg, (x1, y1), (x2, y2), ec, lw)
                print(self.detected)

        try:
            self.prevRects = [(x1, x2, y1, y2, cnt+1, pred) for (x1, x2, y1, y2, cnt, pred) in self.prevRects]
            self.prevRects = [r for r in self.prevRects if r[4] < 60]
        except:
            pass

        self.showFunc(cimg)

        if self.qr_target == 0:
            print('[*] Illegal target')
            self.timer.stop()

        if self.qr_target == current:
            self.prevDirection = self.direction
            self.direction = 0

        if self.direction == 1:
            self.interface.move(0, 0, 0.025, 0)
            return
        elif self.direction == 2:
            self.interface.move(0, -self.v, 0, 0)
            return
        elif self.direction == 3:
            self.interface.move(0, 0, -0.025, 0)
            return
        elif self.direction == 4:
            self.interface.move(0, self.v, 0, 0)
            return

        if self.direction == 0:
            ch, self.task = self.task[0], self.task[1:]

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
            for i in self.sections.li:
                print(i.getPoints())
                print(i.getFound())
            self.stop()

# section 설정을 통한 겹치는 barcode label 정리
        if current is not 0:
            if self.direction == 2:
                sec, ret = self.sections.find('first', current)
                if (sec and ret) is None:
                    if right != 0:
                        self.sections.addSection(current, right, [0,0,0,0])
                sec, ret = self.sections.find('second', current)
                if (sec and ret) is not None:
                    f = sec.getFound()
                    for i in range(len(f)):
                        if f[i] < self.detected[i]:
                            f[i] = self.detected[i]
                    self.sections.modifyAll(sec)

            elif self.direction == 4:
                sec, ret = self.sections.find('second', current)
                if (sec and ret) is None:
                    if left != 0:
                        self.sections.addSection(left, current, [0,0,0,0])
                sec,ret = self.sections.find('first', current)
                if (sec and ret) is not None:
                    f = sec.getFound()
                    for i in range(len(f)):
                        if f[i] < self.detected[i]:
                            f[i] = self.detected[i]
                    self.sections.modifyAll(sec)
                elif self.prevDirection == 2:
                    sec, ret = self.sections.find('second', current)
                    if(sec and ret) is not None:
                        f = sec.getFound()
                        for i in range(len(f)):
                            if f[i] < self.detected[i]:
                                f[i] = self.detected[i]
                        self.sections.modifyAll(sec)

            else:
                if self.prevDirection == 2:
                    sec, ret = self.sections.find('second', current)
                    if (sec and ret) is not None:
                        f = sec.getFound()
                        for i in range(len(f)):
                            if f[i] < self.detected[i]:
                                f[i] = self.detected[i]
                        self.sections.modifyAll(sec)
                elif self.prevDirection == 4:
                    sec,ret = self.sections.find('first', current)
                    if (sec and ret) is not None:
                        f = sec.getFound()
                        for i in range(len(f)):
                            if f[i] < self.detected[i]:
                                f[i] = self.detected[i]
                        self.sections.modifyAll(sec)

            self.detected = [0, 0, 0, 0]
#section 설정 코드 끝

    def initDrone(self):
        self.task = self.default_task[:]

        self.interface = RobotInterface()
        self.qrfinder = QrFinder()

        self.qr_target = 1

        self.v = 0.01

        self.interface.set_target(0.5, 1.45, 0.2, 0)

    def start(self):
        self.initDrone()
        self.timer.start(50, self)

    def stop(self):
        self.interface.stop()
        self.timer.stop()

    def isRunning(self):
        return self.timer.isActive()



class MainWindow(QMainWindow, mainwindow_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.drone_label = []
        self.inputbattery = 100
        self.quitbox = quitBox(self)
        self.learningbox = learningBox(self)
        self.learningbox.hide()
        self.quitbox.hide()
        self.dronepath = None
        self.getGOODS() #제품목록 불러오기
        self.showBettery()
        self.paintTempmap()     #임시 맵 튜
        self.btn_stop.setEnabled(False)

        self.dc = DroneControl(self.showVideo)

    def temp(self):
        self.setBatteryGuage(70)
        self.tableWidget.raise_()
        self.tempMap.raise_()
        self.drone_locate(1, 0)
        
    def drone_path(self):
        self.btn_disalbe()
        self.dronepath = DronePath(self)
        self.dronepath.show()
        
    def showVideo(self, cvImage):
        qimg = QtGui.QImage(cvImage, cvImage.shape[1], cvImage.shape[0], cvImage.strides[0], QtGui.QImage.Format_RGB888)
        self.video_frame.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def start_drone(self):
        if self.dc.isRunning():
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/button/run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon.addPixmap(QtGui.QPixmap(":/button/run2.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.btn_start.setIcon(icon)
            self.btn_start.setIconSize(QtCore.QSize(70, 70))

            self.dc.stop()
        else:
            self.btn_stop.setEnabled(True)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/button/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon.addPixmap(QtGui.QPixmap(":/button/pause2.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
            self.btn_start.setIcon(icon)
            self.dc.start()

    def stop_drone(self):
        self.dc.stop()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/button/run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/button/run2.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon)
        self.video_frame.setPixmap(QtGui.QPixmap(":/drone/그림1.png"))
        self.btn_stop.setEnabled(False)

    def test_drone(self):
        print()

    #공장 맵 그리기
    def paintTempmap(self):
        x, y = 1, 1
        test_moves = ['R', 'R', 'R', 'U', 'L', 'L', 'L', 'U', 'R', 'R', 'R', 'N', 'L', 'L', 'L', 'F']

        #드론 움직임에따른 테이블 그리드 생성
        for direction in test_moves:
            x, y = self.getDroneMoving(x, y, direction)

        #마지막 공백주기
        self.tempMap.insertColumn(self.tempMap.columnCount())
        self.tempMap.insertRow(0)
        #위젯 크기에 맞춰 행렬 사이즈 조정
        i, j = 0, 0
        width = self.tempMap.width() / self.tempMap.columnCount() - 1
        height = self.tempMap.height() / self.tempMap.rowCount() - 1
        while i < self.tempMap.columnCount():
            self.tempMap.setColumnWidth(i, width)
            i += 1
        while j < self.tempMap.rowCount():
            self.tempMap.setRowHeight(j, height)
            j += 1
    def getDroneMoving(self, x, y, dir):
            if (dir == 'N'):
                y += 3
                while y > self.tempMap.rowCount() - 1:
                    self.tempMap.insertRow(0)
            elif (dir == 'S'):
                y -= 2
            elif (dir == 'E'):
                x += 2
            elif (dir == 'W'):
                x -= 2
            elif (dir == 'R'):
                self.addReck(x, y)
                x += 1
                while x > self.tempMap.columnCount() - 1:
                    self.tempMap.insertColumn(x)
            elif(dir == 'L'):
                self.addReck(x, y)
                x -= 1
            elif(dir == 'U' or dir == 'D' or dir == 'F'):
                self.addReck(x, y)

            return x, y
    def addReck(self, x, y):
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(42, 122, 138))
        brush.setStyle(QtCore.Qt.BDiagPattern)
        item.setBackground(brush)
        item.setFlags(QtCore.Qt.ItemIsEditable)
        t = self.tempMap.rowCount() - y - 1
        self.tempMap.setItem(t, x, item)
    def drone_locate(self, x, y):
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEditable)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/drone/drone.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.tempMap.setIconSize(QtCore.QSize(30, 30))
        t = self.tempMap.rowCount() - y - 1
        self.tempMap.setItem(t, x, item)

    #비젼으로 제품 파악 후, 제품이름에 따른 갯수 화면에 표시 --> 인풋값 '제품명' '갯수'
    def setCount_goods(self, itemName, number):
        number = '\t' + str(number)
        i = 0
        while i < self.tableWidget.rowCount():
            temp = self.tableWidget.item(i, 0)
            if(temp.text() == itemName):
                item = QtWidgets.QTableWidgetItem()
                item.setText(number)
                font = QtGui.QFont()
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                brush = QtGui.QBrush(QtGui.QColor(78, 182, 255))
                brush.setStyle(QtCore.Qt.NoBrush)
                item.setForeground(brush)
                self.tableWidget.setItem(temp.row(), 1, item)
                break
            i = i+1

    #제품목록 불러오기
    def getGOODS(self):
        i = 0
        self.tableWidget.clear()
        for dirName in os.listdir("./goods"):
            if(i > 0):
                self.tableWidget.insertRow(i)
            #제품명 등록
            item = QtWidgets.QTableWidgetItem()
            item.setText(dirName)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            brush = QtGui.QBrush(QtGui.QColor(78, 182, 255))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            self.tableWidget.setItem(i, 0, item)
            #checkable 피하기 위한 갯수도 빈칸으로 등록
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 1, item)
            self.tableWidget.resizeColumnsToContents()
            i = i+1

    #드론 라벨 추가
    def add_drone(self):

        dronename = "drone_label" + str(drone_label_count)
        new_drone_label = QtWidgets.QPushButton(self.layoutWidget)
        new_drone_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        new_drone_label.setAutoFillBackground(False)
        new_drone_label.setText("")
        new_drone_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/drone_label/drone_label_clicked.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/drone_label/drone_label.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        new_drone_label.setIcon(icon)
        new_drone_label.setIconSize(QtCore.QSize(200, 80))
        new_drone_label.setCheckable(True)
        new_drone_label.setChecked(True)
        new_drone_label.setAutoRepeat(False)
        new_drone_label.setAutoDefault(False)
        new_drone_label.setObjectName(dronename)

        self.drone_label.append(new_drone_label)
        count = len(self.drone_label) - 1
        self.verticalLayout_drone.removeWidget(self.btn_drone_plus)
        self.verticalLayout_drone.addWidget(self.drone_label[count])
        if (len(self.drone_label) < 4):
            self.verticalLayout_drone.addWidget(self.btn_drone_plus)
        self.dronegroup.addButton(self.drone_label[count])

    #배터리게이지 업데이트 --> 인풋값 0~100
    def setBatteryGuage(self, number):
        self.inputbattery = number
        self.batteryGuage.update()
    #배터리 그리기 메소드
    def showBettery(self):
        self.batteryGuage.initializeGL()
        self.batteryGuage.paintGL = self.paintBattery
    #배터리 대쉬보드 그리기 + 게이지 그리기함수 호출
    def paintBattery(self):
        bettery_in = self.inputbattery
        bettery_out = bettery_in * 0.7 + 50
        glClear(GL_COLOR_BUFFER_BIT)

        glEnable(GL_BLEND) #옵션 활성
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) #알파값 투명하게
        img = cv2.imread('guage.png', cv2.IMREAD_UNCHANGED)
        glDrawPixels(260, 258, GL_BGRA, GL_UNSIGNED_BYTE, img)
        glColor3f(192, 0, 0)

        self.Torus2d(0.63,0.8,bettery_out)
    #배터리 게이지 그리기
    def Torus2d(self, inner, outer, pts):
        glBegin(GL_QUAD_STRIP)
        i = 50
        while i <= pts:
            angle = i / pts * 2 * pi+10
            glVertex2f(inner * cos(angle), inner * sin(angle))
            glVertex2f(outer * cos(angle), outer * sin(angle))
            i = i + 1
        glEnd()

    #태그학습 시작
    def start_learning(self):
        self.btn_disalbe()
        #러닝 시작하는 시그널 보내기
        #게이지 띄우자
        self.learningbox.show()
        #게이지에서 얼마나 됐는지 받아오기

    def turnOffAWS(self):
        self.btn_disalbe()
        self.quitbox.show()

    def btn_enable(self):
        self.btn_turnoff.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.btn_setting.setEnabled(True)
        self.btn_learning.setEnabled(True)
        self.btn_drone_plus.setEnabled(True)
        self.btn_1st.setEnabled(True)
        self.btn_path.setEnabled(True)
    def btn_disalbe(self):
        self.btn_turnoff.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_setting.setEnabled(False)
        self.btn_learning.setEnabled(False)
        self.btn_drone_plus.setEnabled(False)
        self.btn_1st.setEnabled(False)
        self.btn_path.setEnabled(Flase)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mWindow = MainWindow()
    mWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    mWindow.setFixedSize(1348, 864)
    mWindow.show()
    app.exec_()
