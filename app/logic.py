from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QApplication,
    QSystemTrayIcon,
    QMenu

)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
from PyQt6.QtCore import Qt
from app.style import app
from app.CpuUsageMonitor import NetworkMonitoringThread
from app.DiskIOReadandWrite import DiskIORead, DiskIOWrite
from app.MemoryUsage import UsedMem, AvialableMem
from app.NoOfProcess import NumberOfProcesses
from app.WhatIsIp import IP
from app.ISP import ISP
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller temp folder
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class sysmonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SysMonitor')
        self.setWindowIcon(QIcon(
            resource_path("C:/Users/1973r/OneDrive/Desktop/PyQt_apps/sysmonitor/icons/sysmonitor_logo.png")))
        self.setFixedSize(500, 650)
        self.setStyleSheet(app)
        
        
        self.tray_icon = QSystemTrayIcon(QIcon(resource_path("C:/Users/1973r/OneDrive/Desktop/PyQt_apps/sysmonitor/icons/sysmonitor_logo.png")), self)
        self.tray_icon.setToolTip("SysMonitor")

        # Tray menu
        tray_menu = QMenu()

        show_action = QAction("Open", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()

        self.heading_label = QLabel()

        pixmap = QPixmap(
            resource_path("C:/Users/1973r/OneDrive/Desktop/PyQt_apps/sysmonitor/icons/sysmonitor_logo.png")
        )
        scaled_pixmap = pixmap.scaled(
            300, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.heading_label.setPixmap(scaled_pixmap)
        self.heading_label.setScaledContents(True)

        # ---- CPU USAGE MONITORING ---------

        self.labeltext1 = QLabel()
        self.labeltext1.setText('CPU USAGE:')
        self.labeltext1.setFont(QFont('Monospace', 14))

        self.CpuUsage = QLabel()
        self.CpuUsage.setFont(QFont('Monospace', 14))
        self.HandleCpuUsagethread()

        # ------------ DISK MONITORING -----------
        # DISK READ
        self.DiskIOReadText = QLabel()
        self.DiskIOReadText.setText('Disk Read:')
        self.DiskIOReadText.setFont(QFont('Monospace', 14))

        self.DiskIORead = QLabel()
        self.DiskIORead.setFont(QFont('Monospace', 14))
        self.DiskIORead.setStyleSheet('color: white;')

        self.HandleDiskIOreadThread()

        # DISK WRITE
        self.DiskIOWriteText = QLabel()
        self.DiskIOWriteText.setText('Disk Write:')
        self.DiskIOWriteText.setFont(QFont('Monospace', 14))

        self.DiskIOWrite = QLabel()
        self.DiskIOWrite.setFont(QFont('Monospace', 14))
        self.DiskIOWrite.setStyleSheet('color: white;')

        self.HandleDiskIOwriteThread()

        # -------------- MEMORY MONITORING -----------------
        # MEM USAGE
        self.MemUsagetext = QLabel()
        self.MemUsagetext.setText('Memory Used:')
        self.MemUsagetext.setFont(QFont('Monospace', 14))

        self.MemUsage = QLabel()
        self.MemUsage.setFont(QFont('Monospace', 14))

        self.HandleMemUsageThread()

        # TOTAL MEM
        self.MemTotaltext = QLabel()
        self.MemTotaltext.setText('Total Memory:')
        self.MemTotaltext.setFont(QFont('Monospace', 14))

        self.MemTotal = QLabel()
        self.MemTotal.setFont(QFont('Monospace', 14))

        self.HandleTotalMemThread()

        # ------------------ NO. OF PROCESS ----------------------
        self.PidsText = QLabel()
        self.PidsText.setText('Processes:')
        self.PidsText.setFont(QFont('Monospace', 14))

        self.Pids = QLabel()
        self.Pids.setFont(QFont('Monospace', 14))

        self.HandleNoOfProcessCheckerThread()

        # ------------------ IPv4 address ------------------------
        self.IPtext = QLabel()
        self.IPtext.setText('IPv4:')
        self.IPtext.setFont(QFont('Monospace', 14))

        self.ShowIP = QLabel()
        self.ShowIP.setText('Loading...')
        self.ShowIP.setFont(QFont('Monospace', 14))

        self.HandleIpThread()

        # ------------------ ISP ------------------------
        self.ISPtext = QLabel()
        self.ISPtext.setText('ISP:')
        self.ISPtext.setFont(QFont('Monospace', 14))

        self.ShowISP = QLabel()
        self.ShowISP.setText('Loading...')
        self.ShowISP.setFont(QFont('Monospace', 14))

        self.HandleIspThread()

        # Disk Layout ---------------------------------------------------------------------
        disk_layout1 = QHBoxLayout()
        disk_layout1.addWidget(self.DiskIOReadText,
                               alignment=Qt.AlignmentFlag.AlignCenter)
        disk_layout1.addWidget(
            self.DiskIORead, alignment=Qt.AlignmentFlag.AlignCenter)
        # disk_layout.addWidget(self.DiskIOWrite, alignment=Qt.AlignmentFlag.AlignCenter)

        disk_layout2 = QHBoxLayout()
        disk_layout2.addWidget(self.DiskIOWriteText,
                               alignment=Qt.AlignmentFlag.AlignCenter)
        disk_layout2.addWidget(
            self.DiskIOWrite, alignment=Qt.AlignmentFlag.AlignCenter)

        # Memory Layout ------------------------------------------------------------------
        mem_layout1 = QHBoxLayout()
        mem_layout1.addWidget(
            self.MemUsagetext, alignment=Qt.AlignmentFlag.AlignCenter)
        mem_layout1.addWidget(
            self.MemUsage, alignment=Qt.AlignmentFlag.AlignCenter)

        mem_layout2 = QHBoxLayout()
        mem_layout2.addWidget(
            self.MemTotaltext, alignment=Qt.AlignmentFlag.AlignCenter)
        mem_layout2.addWidget(
            self.MemTotal, alignment=Qt.AlignmentFlag.AlignCenter)

        # No. Of Process Layout ------------------------------------------------------
        pids_layout1 = QHBoxLayout()
        pids_layout1.addWidget(
            self.PidsText, alignment=Qt.AlignmentFlag.AlignCenter)
        pids_layout1.addWidget(
            self.Pids, alignment=Qt.AlignmentFlag.AlignCenter)

        # IP Layout ------------------------------------------------------------------
        Ip_layout = QHBoxLayout()
        Ip_layout.addWidget(
            self.IPtext, alignment=Qt.AlignmentFlag.AlignCenter)
        Ip_layout.addWidget(
            self.ShowIP, alignment=Qt.AlignmentFlag.AlignCenter)

        # ISP Layout ------------------------------------------------------------------
        Isp_layout = QHBoxLayout()
        Isp_layout.addWidget(
            self.ISPtext, alignment=Qt.AlignmentFlag.AlignCenter)
        Isp_layout.addWidget(
            self.ShowISP, alignment=Qt.AlignmentFlag.AlignCenter)

        # -------------------------------------------------------------------------------

        layout.addWidget(self.heading_label,
                         alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(
            self.labeltext1, alignment=Qt.AlignmentFlag.AlignCenter)
        hlayout.addWidget(
            self.CpuUsage, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(hlayout)
        layout.addLayout(disk_layout1)
        layout.addLayout(disk_layout2)
        layout.addLayout(mem_layout1)
        layout.addLayout(mem_layout2)
        layout.addLayout(pids_layout1)
        layout.addLayout(Ip_layout)
        layout.addLayout(Isp_layout)

        self.setLayout(layout)

    def HandleCpuUsagethread(self):
        self.cputhread = NetworkMonitoringThread()
        self.cputhread.cpuUsagemonitorthread.connect(self.showcpu_usage)
        self.cputhread.start()

    def showcpu_usage(self, usage):
        Usage = usage
        self.CpuUsage.setText(f'{str(usage)} %')
        if float(Usage) >= 0.0 and float(Usage) <= 50.0:
            self.CpuUsage.setStyleSheet('color: #01E17D;')
        elif float(Usage) > 50.0 and float(Usage) <= 65.0:
            self.CpuUsage.setStyleSheet('color: #E1DD01')
        elif float(Usage) > 65.0 and float(Usage) <= 75.0:
            self.CpuUsage.setStyleSheet('color: #E19B01')
        elif float(Usage) > 75.0 and float(Usage) <= 100.0:
            self.CpuUsage.setStyleSheet('color: #E10101')

    # Disk thread handler ----------------------------
    def HandleDiskIOreadThread(self):
        self.diskioRead = DiskIORead()
        self.diskioRead.diskioread.connect(self.showdiskio_read)
        self.diskioRead.start()

    def showdiskio_read(self, read):
        self.DiskIORead.setText(str(read))

    def HandleDiskIOwriteThread(self):
        self.diskioWrite = DiskIOWrite()
        self.diskioWrite.diskiowrite.connect(self.showdiskio_write)
        self.diskioWrite.start()

    def showdiskio_write(self, write):
        self.DiskIOWrite.setText(str(write))

    # Memory thread handler ----------------------------
    def HandleMemUsageThread(self):
        self.MemoryUsage = UsedMem()
        self.MemoryUsage.memusage.connect(self.showmemusage)
        self.MemoryUsage.start()

    def showmemusage(self, memusage):
        usage = memusage
        self.MemUsage.setText(f'{str(memusage)} GB')
        if float(usage) >= 0.0 and float(usage) <= 50.0:
            self.MemUsage.setStyleSheet('color: #01E17D;')
        elif float(usage) > 50.0 and float(usage) <= 65.0:
            self.MemUsage.setStyleSheet('color: #E1DD01')
        elif float(usage) > 65.0 and float(usage) <= 75.0:
            self.MemUsage.setStyleSheet('color: #E19B01')
        elif float(usage) > 75.0 and float(usage) <= 100.0:
            self.MemUsage.setStyleSheet('color: #E10101')

    def HandleTotalMemThread(self):
        self.TotalMem = AvialableMem()
        self.TotalMem.total.connect(self.showTotalMem)
        self.TotalMem.start()

    def showTotalMem(self, total):
        total_ram = total
        self.MemTotal.setText(f'{str(total)} GB')
        if float(total_ram) >= 0.0 and float(total_ram) <= 4.0:
            self.MemTotal.setStyleSheet('color: #ECBC0F;')
        elif float(total_ram) > 4.0 and float(total_ram) <= 10.0:
            self.MemTotal.setStyleSheet('color: #C3EC0F')
        elif float(total_ram) > 10.0 and float(total_ram) <= 16.0:
            self.MemTotal.setStyleSheet('color: #0FA6EC')
        elif float(total_ram) > 16.0:
            self.MemTotal.setStyleSheet('color: #7F11FC')

    # No of Porcesses checker thread handler -----------------------------
    def HandleNoOfProcessCheckerThread(self):
        self.NoOFPids = NumberOfProcesses()
        self.NoOFPids.numberofprocess.connect(self.showNumOfpids)
        self.NoOFPids.start()

    def showNumOfpids(self, pids):
        self.Pids.setText(str(pids))
        if int(pids) >= 0 and int(pids) <= 100:
            self.Pids.setStyleSheet('color: #50FB17;')
        elif int(pids) > 100 and int(pids) <= 150:
            self.Pids.setStyleSheet('color: #FBFB17;')
        elif int(pids) > 150 and int(pids) <= 200:
            self.Pids.setStyleSheet('color: #FB9417;')
        elif int(pids) > 200:
            self.Pids.setStyleSheet('color: #FB2117;')

    # IP thread handler ----------------------------------------------------
    def HandleIpThread(self):
        self.ipthread = IP()
        self.ipthread.checkip.connect(self.showIPaddress)
        self.ipthread.start()

    def showIPaddress(self, ipv4):
        self.ShowIP.setText(str(ipv4))

    # ISP thread handler -------------------------------------------
    def HandleIspThread(self):
        self.ispthread = ISP()
        self.ispthread.checkisp.connect(self.showISP)
        self.ispthread.start()

    def showISP(self, isp):
        self.ShowISP.setText(str(isp))
    
    # ---------------------------------------------------------------

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "SysMonitor",                    
            "SysMonitor is running in the background!",  
            QSystemTrayIcon.MessageIcon.Information, 
            2000                               
        )


    def show_window(self):
        self.showNormal()
        self.activateWindow()

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
