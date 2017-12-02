# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'learningbox.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(424, 284)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-radius: 10px;")
        self.learningBar = QtWidgets.QProgressBar(Form)
        self.learningBar.setGeometry(QtCore.QRect(90, 200, 261, 21))
        self.learningBar.setStyleSheet("border: 2px solid grey;\n"
"    border-radius: 2px;\n"
"    text-align: center;\n"
"color : rgb(78, 182, 255);\n"
"")
        self.learningBar.setProperty("value", 0)
        self.learningBar.setTextVisible(True)
        self.learningBar.setOrientation(QtCore.Qt.Horizontal)
        self.learningBar.dele
        self.learningBar.setObjectName("learningBar")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(90, 150, 261, 31))
        self.textBrowser.setStyleSheet("color : rgb(78, 182, 255);")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 50, 81, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/button/learningImg.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 421, 281))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/background/frame.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.raise_()
        self.learningBar.raise_()
        self.textBrowser.raise_()
        self.label.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">학습중입니다 잠시만 기다려주십시오</p></body></html>"))

import drone_rc
