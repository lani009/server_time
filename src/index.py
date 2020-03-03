import datetime
import sys
import threading
import time

import requests
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

UIFILE = '../ui/severtimeUI.ui'
ICON = '../ui/icon.png'
class App(QMainWindow):

    clockSignal = pyqtSignal()
    reclick = False

    def __init__(self):
        super().__init__()
        self.threadFlag = False
        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(UIFILE, self)
        self.setWindowTitle("서버시간 알리미")
        self.setWindowIcon(QIcon(ICON))
        self.opacity = QGraphicsOpacityEffect(self.progressBar) #Progress Bar의 투명도 조절을 위함
        self.opacity.setOpacity(0.0)    #시작 시에는 Progress Bar 안보이도록 처리
        self.progressBar.setGraphicsEffect(self.opacity)
        self.show()

    def siteButton(self):
        '''GO! 버튼이 눌렸을 때 실행'''
        url = self.url.toPlainText()
        if(url):
            if self.reclick:
                #Go버튼 재 클릭시 이전에 생성한 thread 종료를 위함.
                self.clock.working = False
            self.reclick = True
            self.opacity.setOpacity(1.0) #Go 버튼 클릭시 Progress Bar 활성화
            self.query = Query(self.url.toPlainText(), self)    #query를 통해 서버 시간을 받아온다.
            self.clock = severClock(self, self.query)   #severClock에게 인수 전달. thread실행시킬 준비를 한다.
            self.clockSignal.connect(self.clock.run)    #custom signal from main to thread
            self.clock.clockChanged.connect(self.updateClock)   #custom signal from thread to main
            self.clock.start() #start the thread
            self.progressBar.setValue(100)
            self.opacity.setOpacity(0.0)    #progress bar 투명화
            self.progressBar.setGraphicsEffect(self.opacity)
        else:
            QMessageBox().critical(self, "경고", "주소창을 채워주세요!")
            return

    def updateClock(self, severTime):
        self.severTime.setText("{}년 {}월 {}일 {}시 {}분 {}초".format(severTime.year, severTime.month, severTime.day, severTime.hour, severTime.minute, severTime.second))

class severClock(QThread):
    working = False
    clockChanged = pyqtSignal(datetime.datetime)

    def __init__(self, App, query):
        super().__init__()
        self.App = App
        self.query = query
        self.working = True

    def run(self):
        while self.working:
            severTime = self.query.getTime()
            self.clockChanged.emit(severTime)
            time.sleep(0.1)


class Query:

    def __init__(self, URL, App):
        self.__App = App
        self.__syncTime(URL)

    def __syncTime(self, URL):
        '''서버와의 시간을 동조'''
        req = requests.get(URL)
        originSec = req.headers["Date"][23:25]
        self.__App.progressBar.setValue(10)
        #지연된 시간
        elapsedTime = req.elapsed
        cnt = 1
        while True:
            #서버로 부터 시간을 받아와 반복문을 통해 시간 오차를 줄인다.
            req = requests.get(URL)
            laterSec = req.headers["Date"][23:25]
            elapsedTime += req.elapsed
            cnt += 1
            if(originSec != laterSec):
                break
            self.__App.progressBar.setValue(54)
        elapsedTime /= cnt
        self.__setTime(req.headers['Date'])

    def __setTime(self, stringTime):
        '''String 시간을 ms로 전환'''
        #서울, 도쿄를 기준으로 +9시간
        koreanTime = datetime.datetime.strptime(stringTime, "%a, %d %b %Y %X GMT") + datetime.timedelta(hours=9)
        self.__timeDelta = koreanTime - datetime.datetime.now()
        self.__App.progressBar.setValue(70)

    def getTime(self):
        severTime = self.__timeDelta + datetime.datetime.now()
        return severTime

    def getYear(self):
        pass

    def getMonth(self):
        pass
    
    def getDate(self):
        pass

    def getDay(self):
        pass

    def getHour(self):
        pass

    def getMinute(self):
        pass

    def getSecond(self):
        pass


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
