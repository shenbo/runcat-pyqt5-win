import threading
import time

from psutil import cpu_percent, virtual_memory
from pystray import Icon, Menu, MenuItem

# PIL dependency simplification
# ref: https://github.com/moses-palmer/pystray/issues/26
class ICOImage:
    def __init__(self, path: str):
        with open(path, 'rb') as file:
            self._data = file.read()
    def save(self, file, format):
        file.write(self._data)

# get cpu usage
def thread_get_usage():
    global cpu_usage, mem_usage
    while True:
        if thread_flag: break
        cpu_usage = cpu_percent(interval=1) / 100
        mem_usage = virtual_memory().percent / 100
        time.sleep(0.5)

def changeMonitor(new_monitor):
    global monitor
    print(monitor, new_monitor)
    if new_monitor != monitor:
        monitor = new_monitor

def on_quit():
    global thread_flag
    thread_flag = 1
    runcat.stop()

# 初始化
monitor = 'CPU'
cpu_usage = 0.2  # 初始化
mem_usage = 0.2  # 初始化
cats = [ICOImage(f'icons/runcat/{i}.ico') for i in range(5)]

menu = (MenuItem(text='CPU', action=lambda: changeMonitor('cpu')),
        MenuItem(text='MEM', action=lambda: changeMonitor('mem')),
        MenuItem(text='QUIT', action=on_quit))
runcat = Icon('run cat', icon=cats[0], title='run cat',  menu=menu)

# 创建两个 threading：一个获取使用率，一个更新图标
thread_flag = 0
threading.Thread(target=runcat.run).start()
threading.Thread(target=thread_get_usage).start()

while True:
    if thread_flag: break
    for icon in cats:
        runcat.icon = icon
        mon = mem_usage if monitor == 'mem' else cpu_usage
        t = 0.2 - mon * 0.15        
        print(f'{mon=:.2%}, {t=:.2f}s, {cpu_usage=:.2%}, {mem_usage=:.2%}')

        tip = f'cpu: {cpu_usage:.2%} \nmem: {mem_usage:.2%}'
        runcat.title = tip

        time.sleep(t)

# pyinstaller -w -i favicon.ico runcat-v0.6-pystray.py --add-data "icons;icons"
