import sys
import threading
import time

import psutil
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon


# === cpu & mem ====
def cpu_mem_func():
    global cpu, mem

    while True:
        cpu = psutil.cpu_percent(interval=1) / 100
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
def update_icon(name, value, icons):
    t = (value * value - 10 * value + 10) / 50
    for i in range(5):
        tray.setIcon(icons[i])
        tray.setToolTip(f'{name}: {value:.2%}')
        time.sleep(t)


# === threading ====
cpu, mem = 0.1, 0.1
timer = threading.Timer(1, cpu_mem_func, [])
timer.start()

icons = [QIcon(f'icons/{i}.png') for i in range(5)]

while True:
    update_icon('cpu', cpu, icons)

# app.exec_()

# pyinstaller -w -i favicon.ico -F runcat.py
# pyinstaller -w -i favicon.ico runcat.py
