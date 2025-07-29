from PyQt6.QtCore import QThread, pyqtSignal
import psutil
import time

class NumberOfProcesses(QThread):
    numberofprocess = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.check_no_of_process()

    def check_no_of_process(self):
        while True:
            check = len(psutil.pids())
            self.numberofprocess.emit(str(check))
            time.sleep(1)
    