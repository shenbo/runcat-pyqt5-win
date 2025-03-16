import os
import sys
import threading
import time
import base64

import psutil
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

# import pynvml

# pynvml.nvmlInit()
# handle = pynvml.nvmlDeviceGetHandleByIndex(0)   # GPU id: 0

cpu = "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAABv0lEQVRYhe2YsU7CQBzGvx5tIjAYUCcHFxPF0AQWEhNjMK4y+AC8BqMPwFsIj6BxNoSJmHSoUQYnHRgMJAyUgfbOQWmgnBR6tBTSL2nSy93979e77y7/HhBySW4NBo0KG78nL6vSqstu4xP3bwASWdXXsjDgOhV6QK4Hzq9vbyilNcZoKhAIEutZpll+aTw+OetkXgfK2P3u4VFK2Yn7TwdgNDTS/c5nDcC+s467xIxa6aDgAECJJ8Ao3ePVhd6DMjB91gHA1d37VKOLQg55NQNNb6PZ0oQGnBfLyZG8rEr2DCayqv04lVczUBQZOfVECM4tFo/B3iTGq/5vUE1vI6+eQtPbwoDzYvEYuMdMoVhiB8dnwjDL6PvjDa3nhxmehTwYlHgetJd42nvrAZxkGC/3Qh4MSjwGGZhNewrFEptpGYB46VfkwWUUeVBUkQdFFXlQVJEHRbW9Hgwq5ffswck0XRRwXizPHgwq5ffswWZLE565RWJt5DnI/XGXSKw3Ghr+E/1pNDQgEdLl1XHvZizTLPc7X3VGrbS/aL+SCOlaFi176jxoVBjr1dl4h6267KbQ381sB6Bz+6+6vNH6AQRbX1EHaRVCAAAAAElFTkSuQmCC"
mem = "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAABX0lEQVRYhe2WPUvDYBCAn8QirdVI6wfoIA4Oori6uLjopIOzKBT9DYq/QHRzV9Hi7iA4u+jiKNoOgoNUKIJDxA8KvddBW6omtk2CSeF9lgt34XjIm8sFNBrNnxgAmf2NOYXKikgqbCGANtN4Uoa5dJDZPI19puRwfHgoZSUT4Zp9Yb++pa/v7rNArwlQFpWOihyA1ZFARHoAzLBl6hF5wZhTcm/9+FduZWuh4XpQPVwFAfpGxqrXj7c3TdeD6hH5I9aCftGCftGCftGCfom8oOuqc1s9jdaD6mEALO+uqamJ0bo3/yfnV3myq9tG5I9YC/olBpA/ypEnF7aLI9Uprv15jAKVCXf9zDRL6eVZ7OLDOwZY/YPx9mRXIK/PtyY7i52eIoBdLJQENVMWmbWLhVIQPeHHExzoNj1FACUSvzw7uQCYnJ6PB9ETWmCKW0ewMjVeotNOrc17jRqNpgE+AFQ/pkPkXJ2GAAAAAElFTkSuQmCC"
gpu = "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAE5klEQVRYhe2Ya0xTZxjHfz2Hcm1xKGBB58QLTARRuW2oixcYOlnMYtBlbt7wEpcsy5I5N3WZH4zOKR+mBhNxDjYvEeaMRucUtzgnTIo47qJGGRe5JpZLS2lpe/YB2zGpVBojxPj71PdJ+/SXPv9z3vcUXvCcI/t89yEJQBRFvSAI50XJkrLtk1Wtgy1mxQVgw8olGI3dHrnqoqS71XXfAYsH2cuGAHAgM1vKVRfpZ8RMdTWbLQsGW6o3wtcb18hMklx5516N6Ooqx2Ixewy2VG9cAPZsXK7bknrYVlx+6DNpUGRcxGbJwu7vV+1MRYZkE3yU9+MTn63ZQ9q0Wv8/S4u3rTj0hTGTnXvhYQaHCsMUCmaET/GSy2WbrLUhJQjg46XEaDYFWNd2R2zl9+yqJ248NzmoT02yQIm6kpK8O9Tdq0ffacBL4c6ooAAi4kIIiw5G9uhPJAMkZE8kCD33SEccyMjqU3vQ0sbxfeeQi55Mj3odpcc/XM//i/ETJzM2aAJ55/O4cq6Q9z5aiI+f92N7OxS09+WOeNDSRvr2bGbOimdadCwAxYUFALwaGsa4CcGEhk+hsOAaB7dns25r8mMl+xW0NzZHSBY4+u1ZVKrRRERG2+pabQcASu9htlrIpMk03L9PZuppPt7xQd9xOxJ0JoPF+ZVomttpMrZwKusYSe8k4+bmhqu7O+7uHhgMBlo1Gi7/doHK8lIsFgvKYd6UXb9NeEzwwARh4BksybtN3BuzuXb1D27dLOd+XQ3Rr81k0pRpiKJAQ1MjxedO09xQjyiKTAyZhM/w4RTn3nJOcKAZbKhpYn7iUkLDIjjzcxZ1tdXI5HLeTpxNoMqP+sZmTCYTvr5+xCe+hULpTUdHOxnp++z2e+oZ7NR24eHphSiKLE9ZT9XdO2ja2whU+QEQqPLHzc2VWbPnolD2XBgenp7odfqBCzqTQU+FO/pOHQqlN91GIzcrShnur6K+sZlAlT/1Dc0YDAbS0/YydXoU8xIX0qXvxMPL/hnlqWdw1FgV19X5GLr0lJcW0aXX4zdShSiKCIKA2WymXaNBQMaNgnxqq6uJjIll9LgAu72fegYj4kI4++MVdFotAGPGjmNB0iI0rRrO/HSCUWNeYemyFURGxXAq6xgtzY1cvnSRRavnDFzQmQyGRQdzITuXiaNDeWPOPEaqAgHQ6XR0denpNhoB8PXzZ9nKtZw4koEkGAmL6nsFOxR0JoMyAVI2Lebg9izqamtsgu1tPY85CqXS9pmKshK0nW2s/zLZ7k3aoSA4txf7+HmzbusSju//hYrSv4mMjuNWZQUAI0b4Ul5aRKE6D0noZv3WZF4a8Yz3Yqvkhq/epazgNsV5BdTVNiATZNwovMbL4wOYkRROWJSd08xABJ3JYG9kAoTHBhMeaz9fdpHAetyHIXhg1WjbcXVxqbeuh5Rgq7aDq2UlOpPJvMtaszviI5cuPDurXshFsckiSbsyVu/aT0pPza7gD2u+kQGkbY6XEmJ6cpijruLDHZdkABfT50sJi5cBcGBPJgkxQeSoq9jw6Yo+a4Cck0d5c+2v/+vZu18fVv/3clBHnLY5XkrbHN/vM/igCSbEBGGdTn84vA/mqO3vJjknj/Z5j7X26PpJe/bLltTDhuqWdsn6d9xQwTZii2SRnN01XvCC55l/Ad8D3jitK/mLAAAAAElFTkSuQmCC"
quit = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAAS1BMVEUAAABaWlpYWFhZWVlYWFhdXV1tbW1ZWVlZWVlaWlpYWFheXl5ZWVlZWVlYWFhYWFhZWVlYWFhZWVlZWVlaWlpZWVldXV1dXV1YWFj2jWLcAAAAGHRSTlMARPvZnCcH7rqRZxPy69/Er4hwX0o8IQuCS26JAAAAZUlEQVQY05VQ1w6AQAjz9nLP/v+XqlFiThLN8UIDoS2tikqIjaAV4kYanoY9NK09woUGdJb2SSGefUKbHlbj5MG1yNpkWtKZtZFz7iBCKYxvXwEkzIa/51yIW+Lmv97kgfDoSmoH5W0EwcHlwF4AAAAASUVORK5CYII="
runcat = [
    "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",
]
mario = [
    "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",
]


def base64_to_icon(base64_string):
    # 解码 Base64 字符串为二进制数据
    image_data = base64.b64decode(base64_string)
    # 创建 QPixmap 对象并加载二进制图像数据
    pixmap = QPixmap()
    pixmap.loadFromData(image_data)
    # 从 QPixmap 创建 QIcon
    icon = QIcon(pixmap)
    return icon


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.monitor = "cpu"
        self.cpu_usage = 0.2  # 初始化
        self.mem_usage = 0.2  # 初始化
        self.gpu_usage = 0.2  # 初始化

        self.icon_type = "runcat"  # 设定默认图标，并加载
        self.icon_list = self.loadIcon()
        self.setIcon(self.icon_list[0])

        self.setVisible(True)
        self.setMenu()  # 加载菜单
        self.updateIcon()  # 更新图标

    # 加载图标
    def loadIcon(self):
        if self.icon_type == "mario":
            return [base64_to_icon(s) for s in mario]
        return [base64_to_icon(s) for s in runcat]

    # 设置菜单
    def setMenu(self):
        self.menu = QMenu()

        self.action_1 = QAction(base64_to_icon(runcat[0]), "cat", self, triggered=lambda: self.changeIconType("runcat"))
        self.action_2 = QAction(base64_to_icon(mario[0]), "mario", self, triggered=lambda: self.changeIconType("mario"))
        self.action_c = QAction(base64_to_icon(cpu), "cpu", self, triggered=lambda: self.changeMonitor("cpu"))
        self.action_m = QAction(base64_to_icon(mem), "memory", self, triggered=lambda: self.changeMonitor("mem"))
        # self.action_g = QAction(base64_to_icon(gpu), 'gpu', self, triggered=lambda: self.changeMonitor('gpu'))
        self.action_q = QAction(base64_to_icon(quit), "quit", self, triggered=self.quit)

        self.menu.addAction(self.action_c)
        self.menu.addAction(self.action_m)
        # self.menu.addAction(self.action_g)
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
            # meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            # self.gpu_usage = meminfo.used / meminfo.total
            # print(self.cpu_usage)
            time.sleep(0.5)

    # update icon
    def thread_update_icon(self):
        while True:
            mon = self.cpu_usage
            if self.monitor == "mem":
                mon = self.mem_usage
            elif self.monitor == "gpu":
                mon = self.gpu_usage

            t = 0.2 - mon * 0.15
            # print(mon, t)
            for i in self.icon_list:
                self.setIcon(i)
                tip = f"cpu: {self.cpu_usage:.2%} \nmem: {self.mem_usage:.2%}"
                self.setToolTip(tip)
                # print(i, self.monitor, f'{self.cpu_usage}:.2%')
                time.sleep(t)

    # Change icon type
    def changeIconType(self, new_icon_type):
        print(new_icon_type)
        if new_icon_type != self.icon_type:
            self.icon_type = new_icon_type
            self.icon_list = self.loadIcon()
            print(f"Load {self.icon_type}({len(self.icon_list)}) icons...")

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

    sys.exit(app.exec())


#
# pyinstaller -w -i favicon.ico -F "runcat-v1.0-nogpu(pyqt6).py"
#
