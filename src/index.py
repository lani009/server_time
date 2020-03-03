import datetime
import sys

import requests
from PyQt5 import uic
from PyQt5.QtWidgets import *

UIFILE = '../ui/severtimeUI.ui'
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("서버시간 알리미")
        self.ui = uic.loadUi(UIFILE, self)

        self.show()

    def siteButton(self):
        '''GO! 버튼이 눌렸을 때 실행'''
        #QMessageBox().information(title="경고", text="페이지를 입력해 주세요!")
        self.query = Query(self.url.toPlainText())


class Query:
    day={
        "Mon" : "월",
        "Tue" : "화",
        "Wed" : "수",
        "Thu" : "목",
        "Fri" : "금",
        "Sat" : "토",
        "Sun" : "일"
    }
    month={
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May" : 5,
        "Jun" : 6,
        "Jul" : 7,
        "Aug" : 8,
        "Sep" : 9,
        "Oct" : 10,
        "Nov" : 11,
        "Dec" : 12
    }
    headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    def __init__(self, URL):
        self.__syncTime(URL)

    def __syncTime(self, URL):
        '''서버와의 시간을 동조'''
        req = requests.get(URL)
        originSec = req.headers["Date"][23:25]
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
        
        elapsedTime /= cnt
        self.__setTime(req.headers['Date'])

    def __setTime(self, stringTime):
        '''String 시간을 ms로 전환'''
        #서울, 도쿄를 기준으로 +9시간
        koreanTime = datetime.datetime.strptime(stringTime, "%a, %d %b %Y %X GMT") + datetime.timedelta(hours=9)


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
