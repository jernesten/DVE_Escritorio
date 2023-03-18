import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.trayIcon = QSystemTrayIcon(QIcon("img/logo-ico.png"), self)
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        self.trayIcon.show()
        self.disambiguateTimer = QTimer(self)
        self.disambiguateTimer.setSingleShot(True)
        self.disambiguateTimer.timeout.connect(
                self.disambiguateTimerTimeout)

    def onTrayIconActivated(self, reason):
        print ("onTrayIconActivated:"), reason
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguateTimer.start(qApp.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguateTimer.stop()
            print ("Tray icon double clicked")

    def disambiguateTimerTimeout(self):
        print ("Tray icon single clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())