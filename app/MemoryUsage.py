from PyQt6.QtCore import QThread, pyqtSignal
import psutil
import time

# Memory Usage Check --------------------
class UsedMem(QThread):
    memusage = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.checkmemusage()

    def checkmemusage(self):
        while True:
            used_memory = psutil.virtual_memory()
            check = used_memory.used / (1024 ** 3)
            output = f'{check:.2f}'
            self.memusage.emit(str(output))
            time.sleep(1)
            

# Available Memory Check -------------------- 
class AvialableMem(QThread):
    total = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.checktotalmem()

    def checktotalmem(self):
        while True:
            total_mem = psutil.virtual_memory()
            check = total_mem.total / (1024 ** 3)
            output = f'{check:.2f}'
            self.total.emit(str(output))
            time.sleep(1)
    