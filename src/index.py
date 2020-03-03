import datetime
import sys
import threading
import time

import requests
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

UIFILE = '../ui/severtimeUI.ui'
class App(QMainWindow):

    clockSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.threadFlag = False
        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(UIFILE, self)
        self.setWindowTitle("서버시간 알리미")
        self.show()

    def siteButton(self):
        '''GO! 버튼이 눌렸을 때 실행'''
        url = self.url.toPlainText()
        if(url):
            self.query = Query(self.url.toPlainText(), self)    #query를 통해 서버 시간을 받아온다.
            self.clock = severClock(self, self.query)   #severClock에게 인수 전달. thread실행시킬 준비를 한다.
            self.clockSignal.connect(self.clock.run)    #custom signal from main to thread
            self.clock.clockChanged.connect(self.updateClock)   #custom signal from thread to main
            self.clock.start() #start the thread
            self.progressBar.setValue(100)
        else:
            #QMessageBox().information(title="경고", text="페이지를 입력해 주세요!")
            return

    def updateClock(self, severTime):
        self.severTime.setText("{}년 {}월 {}일 {}시 {}분 {}초".format(severTime.year, severTime.month, severTime.day, severTime.hour, severTime.minute, severTime.second))

class severClock(QThread):
    
    clockChanged = pyqtSignal(datetime.datetime)

    def __init__(self, App, query):
        super().__init__()
        self.App = App
        self.query = query

    def run(self):
        while True:
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
