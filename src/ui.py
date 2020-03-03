# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\severtimeUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 180)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.query = QtWidgets.QPushButton(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(610, 10, 91, 51))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        self.query.setFont(font)
        self.query.setMouseTracking(False)
        self.query.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.query.setAutoFillBackground(False)
        self.query.setCheckable(False)
        self.query.setChecked(False)
        self.query.setObjectName("query")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 80, 741, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.infoLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.infoLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.infoLayout.setContentsMargins(10, 10, 10, 0)
        self.infoLayout.setHorizontalSpacing(15)
        self.infoLayout.setVerticalSpacing(20)
        self.infoLayout.setObjectName("infoLayout")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser_2.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.textBrowser_2.setPlaceholderText("")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.infoLayout.addWidget(self.textBrowser_2, 0, 0, 1, 1)
        self.severTime = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        self.severTime.setFont(font)
        self.severTime.setObjectName("severTime")
        self.infoLayout.addWidget(self.severTime, 0, 1, 1, 1)
        self.infoLayout.setColumnStretch(1, 1)
        self.infoLayout.setRowStretch(0, 2)
        self.url = QtWidgets.QTextEdit(self.centralwidget)
        self.url.setGeometry(QtCore.QRect(100, 10, 481, 51))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.url.setFont(font)
        self.url.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.url.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.url.setStyleSheet("")
        self.url.setObjectName("url")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(100, 68, 481, 16))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.query.clicked.connect(MainWindow.siteButton)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.query.setText(_translate("MainWindow", "GO!"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">서버시간</p></body></html>"))
        self.url.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:18pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.url.setPlaceholderText(_translate("MainWindow", "https://naver.com"))

