from PyQt6.QtWidgets import QApplication
from app.logic import sysmonitor
import sys

def run():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) 
    win = sysmonitor()
    win.show()
    app.exec()

if __name__ == '__main__':
    run()