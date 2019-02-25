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

# Create Qt App
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
# Create trayicon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('0.ico'))
tray.setVisible(True)

gpu = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (gpu * gpu - 10 * gpu + 10) / 40
    for i in range(5):
        # Update trayicon
        tray.setIcon(QIcon('{}.ico'.format(i)))
        tray.setToolTip('GPU: {:.2%}'.format(gpu))
        time.sleep(t)

app.exec_()

# pyinstaller --onefile -w -i 2.ico -F runcat.py
