import sys
import time
import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)   # GPU id: 0

# Get gpu usage
def func():
    while True:
        global gpu
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu = meminfo.used / meminfo.total
        time.sleep(1)


# Create pyqt app
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create system tray icon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('icons/runcat/0.png'))
tray.setVisible(True)

# Update tray icon
gpu = 0.2
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = 0.2 - gpu * 0.15
    for i in range(5):
        tray.setIcon(QIcon(f'icons/runcat/{i}.png'))
        tray.setToolTip(f'gpu: {gpu:.2%}')
        time.sleep(t)

app.exec_()
