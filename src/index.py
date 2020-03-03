import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("서버시간 알리미")
        self.ui = uic.loadUi("./severtimeUI.ui")
        self.show()


    def siteButton(self):
        pass


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   sys.exit(app.exec_())