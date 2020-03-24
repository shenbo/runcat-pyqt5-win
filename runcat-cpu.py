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
tray.setIcon(QIcon('icons/runcat/0.png'))
tray.setVisible(True)

# Update tray icon
cpu = 0.2
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = 0.2 - cpu * 0.15
    for i in range(5):
        tray.setIcon(QIcon(f'icons/runcat/{i}.png'))
        tray.setToolTip(f'cpu: {cpu:.2%}')
        time.sleep(t)

app.exec_()

# pyinstaller -w -i favicon.ico -F runcat-cpu.py
# pyinstaller -w -i favicon.ico runcat-cpu.py
