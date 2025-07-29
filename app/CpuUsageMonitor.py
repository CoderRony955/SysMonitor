from PyQt6.QtCore import QThread, pyqtSignal
import psutil

class NetworkMonitoringThread(QThread):
    cpuUsagemonitorthread = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.check_cpu_ussage()

    def check_cpu_ussage(self):
        while True:
            check = psutil.cpu_percent(interval=1)
            self.cpuUsagemonitorthread.emit(str(check))
    