import os
import sys
import threading
import time

import psutil
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)   # GPU id: 0


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.monitor = 'cpu'
        self.cpu_usage = 0.2  # 初始化
        self.mem_usage = 0.2  # 初始化
        self.gpu_usage = 0.2  # 初始化

        self.icon_type = 'runcat'         # 设定默认图标，并加载
        self.icon_list = self.loadIcon()
        self.setIcon(self.icon_list[0])

        self.setVisible(True)
        self.setMenu()  # 加载菜单
        self.updateIcon()  # 更新图标

    # 加载图标
    def loadIcon(self):
        if self.icon_type == 'mario':
            return [QIcon(f'icons/{self.icon_type}/{i}.png') for i in range(3)]
        return [QIcon(f'icons/{self.icon_type}/{i}.png') for i in range(5)]

    # 设置菜单
    def setMenu(self):
        self.menu = QMenu()

        self.action_1 = QAction(QIcon(f'icons/cat.png'), 'cat', self, triggered=lambda: self.changeIconType('runcat'))
        self.action_2 = QAction(QIcon(f'icons/mario/0.png'), 'mario', self, triggered=lambda: self.changeIconType('mario'))

        self.action_c = QAction(QIcon(f'icons/cpu.png'), 'cpu', self, triggered=lambda: self.changeMonitor('cpu'))
        self.action_m = QAction(QIcon(f'icons/mem.png'), 'memory', self, triggered=lambda: self.changeMonitor('mem'))
        self.action_g = QAction(QIcon(f'icons/gpu.png'), 'gpu', self, triggered=lambda: self.changeMonitor('gpu'))

        self.action_q = QAction(QIcon(f'icons/quit.png'), 'quit', self, triggered=self.quit)

        self.menu.addAction(self.action_c)
        self.menu.addAction(self.action_m)
        self.menu.addAction(self.action_g)
        self.menu.addSeparator()
        self.menu.addAction(self.action_1)
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_q)

        self.setContextMenu(self.menu)

    # 根据使用率更新图标，
    # 创建两个 threading：一个获取使用率，一个更新图标
    def updateIcon(self):
        threading.Timer(0.1, self.thread_get_cpu_usage, []).start()
        threading.Timer(0.1, self.thread_update_icon, []).start()

    # get cpu usage
    def thread_get_cpu_usage(self):
        while True:
            self.cpu_usage = psutil.cpu_percent(interval=1) / 100
            self.mem_usage = psutil.virtual_memory().percent / 100
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            self.gpu_usage = meminfo.used / meminfo.total
            # print(self.cpu_usage)
            time.sleep(0.5)

    # update icon
    def thread_update_icon(self):
        while True:
            mon = self.cpu_usage
            if self.monitor == 'mem':
                mon = self.mem_usage
            elif self.monitor == 'gpu':
                mon = self.gpu_usage
            
            t = 0.2 - mon * 0.15
            # print(mon, t)
            for i in self.icon_list:
                self.setIcon(i)
                tip = f'cpu: {self.cpu_usage:.2%} \nmem: {self.mem_usage:.2%} \ngpu: {self.gpu_usage:.2%}'
                self.setToolTip(tip)
                # print(i, self.monitor, f'{self.cpu_usage}:.2%')
                time.sleep(t)

    # Change icon type
    def changeIconType(self, new_icon_type):
        print(new_icon_type)
        if new_icon_type != self.icon_type:
            self.icon_type = new_icon_type
            self.icon_list = self.loadIcon()
            print(f'Load {self.icon_type}({len(self.icon_list)}) icons...')

    # change monitor type
    def changeMonitor(self, new_monitor):
        print(self.monitor, new_monitor)
        if new_monitor != self.monitor:
            self.monitor = new_monitor

    # 退出程序
    def quit(self):
        self.setVisible(False)
        app.quit()
        os._exit(-1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = TrayIcon()

    sys.exit(app.exec_())


#
# pyinstaller -w -i favicon.ico runcat-v0.3.py --add-data "icons;icons"
