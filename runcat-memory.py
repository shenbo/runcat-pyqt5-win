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

# Create Qt App
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
# Create trayicon
tray = QSystemTrayIcon()
tray.setIcon(QIcon('0.ico'))
tray.setVisible(True)

mem = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (mem * mem - 10 * mem + 10) / 40
    for i in range(5):
        # Update trayicon
        tray.setIcon(QIcon('{}.ico'.format(i)))
        tray.setToolTip('Memory: {:.2%}'.format(mem))
        time.sleep(t)

app.exec_()

# pyinstaller --onefile -w -i 2.ico -F runcat-memory.py
