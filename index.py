import datetime
import sys
import threading
import time
from winsound import Beep

import requests
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

UIFILE = './ui/severtimeUI.ui'
ICON = './ui/icon.png'
class App(QMainWindow):

    clockSignal = pyqtSignal()
    reclick = False
    doAlarm = False

    def __init__(self):
        super().__init__()
        self.threadFlag = False
        self.initUI()

    def initUI(self):
        self.ui = uic.loadUi(UIFILE, self)
        self.setWindowTitle("서버시간 알리미 v0.1")
        self.setWindowIcon(QIcon(ICON))
        self.setFixedSize(800, 200) #사이즈 고정

        self.opacity = QGraphicsOpacityEffect(self.progressBar) #Progress Bar의 투명도 조절을 위함
        self.opacity.setOpacity(0.0)    #시작 시에는 Progress Bar 안보이도록 처리
        self.progressBar.setGraphicsEffect(self.opacity)

        self.show()

    @pyqtSlot()
    def opacityChanged(self):
        self.setWindowOpacity((120-self.opacitySlider.value()) / 100)
    
    @pyqtSlot(int)
    def fixWindow(self, state):
        flags = self.windowFlags()
        if state == 2:
            self.setWindowFlags(flags | Qt.X11BypassWindowManagerHint | Qt.WindowStaysOnTopHint)  
        else:
            self.setWindowFlags(flags & ~(Qt.X11BypassWindowManagerHint | Qt.WindowStaysOnTopHint))

        self.show()

    @pyqtSlot()
    def isEnter(self):
        text = self.url.toPlainText()
        if '\n' in text:
            self.url.setPlainText(text[0:len(text)-1])
            self.siteButton()

    @pyqtSlot()
    def siteButton(self):
        '''GO! 버튼이 눌렸을 때 실행'''
        self.progressBar.setValue(0)
        self.opacity.setOpacity(1.0) #Go 버튼 클릭시 Progress Bar 활성화
        self.progressBar.setGraphicsEffect(self.opacity)
        url = self.url.toPlainText()
        if(url):
            if self.reclick:
                #Go버튼 재 클릭시 이전에 생성한 thread 종료를 위함.
                self.clock.working = False
            
            try:
                self.query = Query(self.url.toPlainText(), self)    #query를 통해 서버 시간을 받아온다.
            except Exception as e:
                self.url.setText("")
                print(e)
                QMessageBox().critical(self, "주소로 부터 응답 없음", "옳지 않은 주소이거나, 인터넷 상태가 불량합니다")
                return

            self.clock = severClock(self, self.query)   #severClock에게 인수 전달. thread실행시킬 준비를 한다.
            self.clockSignal.connect(self.clock.run)    #custom signal from main to thread
            self.clock.clockChanged.connect(self.updateClock)   #custom signal from thread to main
            self.clock.start() #start the thread
            self.progressBar.setValue(100)
            self.opacity.setOpacity(0.0)    #progress bar 투명화
            self.progressBar.setGraphicsEffect(self.opacity)
            self.reclick = True
        else:
            QMessageBox().critical(self, "경고", "주소창을 채워주세요.")
            return

    @pyqtSlot()
    def setAlarm(self):
        if not self.reclick:
            #사이트 등록이 되어 있지 않으면, 경고뜸
            QMessageBox().critical(self, "경고", "사이트를 먼저 등록해 주세요.")
            return
        
        if self.doAlarm:
            alarmVerify = QMessageBox(self)
            result = alarmVerify.question(self, "알람 취소", "알람을 취소하겠습니까?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.doAlarm = False
                self.alarmButton.setText("알람등록")
            
            return
        else:
            #알람설정 눌렀을 때 예 아니오 질문창
            alarmVerify = QMessageBox(self)
            result = alarmVerify.question(self, '알람 등록', '알람을 등록하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.No:
                return
            self.alarmButton.setText("알람취소")
        
        self.doAlarm = True #시간 업데이트 될 때마다 알람 할지 말지. 플래그변수
        currentAlarmNoon = self.alarmNoon.currentIndex()
        currentAlarmHour = self.alarmHour.currentIndex()
        currentAlarmMinute = self.alarmMinute.currentIndex()
        currentAlarmSecond = self.alarmSecond.currentIndex()

        if currentAlarmNoon == 1:
            currentAlarmHour += 12
        self.alarmTime = datetime.datetime(
                year=1, month=1, day=1,
                hour=currentAlarmHour + 1, minute=currentAlarmMinute,second=currentAlarmSecond
        )
        
        self.alarmThread = threading.Thread(target=self.alarm)  #알람 울릴거 대비해서 미리 쓰레드 선언 해놓음
        

    def updateClock(self, severTime):
        self.severTime.setText("{}년 {}월 {}일 {}시 {}분 {}초".format(severTime.year, severTime.month, severTime.day, severTime.hour, severTime.minute, severTime.second))
        if self.doAlarm:
            self.alarmTime = self.alarmTime.replace(year=severTime.year, month=severTime.month, day=severTime.day)
            self.checkAlarm(severTime)
    
    def checkAlarm(self, severTime):
        '''알람 울릴 시간이 되면, 알람 쓰레드 생성시킴.'''
        timeDelta = self.alarmTime - severTime
        if timeDelta.seconds <= 2:
            self.alarmThread.start()
            self.doAlarm = False
            self.alarmButton.setText("알람등록")
    
    def alarm(self):
        Beep(450,500)
        time.sleep(0.5)
        Beep(450,500)
        time.sleep(0.5)
        Beep(450,500)
        time.sleep(0.5)
        Beep(880,1500)


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
        #elapsedTime = req.elapsed
        cnt = 1
        while True:
            #서버로 부터 시간을 받아와 반복문을 통해 시간 오차를 줄인다.
            req = requests.get(URL)
            laterSec = req.headers["Date"][23:25]
            #elapsedTime += req.elapsed
            cnt += 1
            QProgressBar.value
            self.__App.progressBar.setValue(self.__App.progressBar.value() + 7)
            if(originSec != laterSec):
                break
        #elapsedTime /= cnt
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

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())
