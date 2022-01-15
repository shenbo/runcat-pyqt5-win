import sys
import time
import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

import psutil


# Get memory usage
def func():
    while True:
        global mem
        mem = psutil.virtual_memory().percent / 100
        time.sleep(1)


# Create pyqt app
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create system tray icon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('icons/runcat/0.png'))
tray.setVisible(True)

# Update tray icon
mem = 0.2
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = 0.2 - mem * 0.15
    for i in range(5):
        tray.setIcon(QIcon(f'icons/runcat/{i}.png'))
        tray.setToolTip(f'memory: {mem:.2%}')
        time.sleep(t)

app.exec_()
