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
tray.setIcon(QIcon('icons/0.png'))
tray.setVisible(True)

# Update tray icon
gpu = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (gpu * gpu - 10 * gpu + 10) / 50
    for i in range(5):
        tray.setIcon(QIcon('icons/g{}.png'.format(i)))
        tray.setToolTip('GPU: {:.2%}'.format(gpu))
        time.sleep(t)

app.exec_()

# pyinstaller -w -i favicon.ico -F runcat.py
# pyinstaller -w -i favicon.ico runcat.py
