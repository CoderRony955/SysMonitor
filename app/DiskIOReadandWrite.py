from PyQt6.QtCore import QThread, pyqtSignal
import psutil
import time

# Read Thread --------------------
class DiskIORead(QThread):
    diskioread = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.checkdiskioread()

    def checkdiskioread(self):
        while True:
            io = psutil.disk_io_counters()
            read_output = io.read_bytes / (1024 *1024)
            self.diskioread.emit(f'{str(round(read_output))} MB')
            time.sleep(1)
            

# Write Thread -------------------- 
class DiskIOWrite(QThread):
    diskiowrite = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        self.checkdiskiowrite()

    def checkdiskiowrite(self):
        while True:
            io = psutil.disk_io_counters()
            write_output = io.write_bytes / (1024 *1024)
            self.diskiowrite.emit(f'{str(round(write_output))} MB')
            time.sleep(1)
    