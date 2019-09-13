import sys
import time
import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

import psutil


# Get cpu usage
def func():
    while True:
        global cpu
        cpu = psutil.cpu_percent(interval=1) / 100
        time.sleep(1)


# Create pyqt app
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create system tray icon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('icons/0.png'))
tray.setVisible(True)

# Update tray icon
cpu = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (cpu * cpu - 10 * cpu + 10) / 50
    for i in range(5):
        tray.setIcon(QIcon(f'icons/{i}.png'))
        tray.setToolTip(f'CPU: {cpu:.2%}')
        time.sleep(t)

app.exec_()

# pyinstaller -w -i favicon.ico -F runcat.py
# pyinstaller -w -i favicon.ico runcat.py
