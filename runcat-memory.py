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
tray.setIcon(QIcon('icons/0.png'))
tray.setVisible(True)

# Update tray icon
mem = 0.1
timer = threading.Timer(1, func, [])
timer.start()

while True:
    t = (mem * mem - 10 * mem + 10) / 40
    for i in range(5):
        tray.setIcon(QIcon('icons/g{}.png'.format(i)))
        tray.setToolTip('memory: {:.2%}'.format(mem))
        time.sleep(t)

app.exec_()

# pyinstaller -w -i favicon.ico -F runcat.py
# pyinstaller -w -i favicon.ico runcat.py
