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

# Create Qt App
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
# Create trayicon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('0.ico'))
tray.setVisible(True)

cpu = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (cpu * cpu - 10 * cpu + 10) / 40
    for i in range(5):
        # Update trayicon
        tray.setIcon(QIcon('{}.ico'.format(i)))
        tray.setToolTip('CPU: {:.2%}'.format(cpu))
        time.sleep(t)

app.exec_()

# pyinstaller --onefile -w -i 2.ico -F runcat.py
