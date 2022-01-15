import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)   # 高分屏
import threading
import time

import psutil
from infi.systray import SysTrayIcon

import pynvml

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)    # GPU id: 0

thread_flags = 1                                 # 多线程标记

monitor = 'cpu'
cpu_usage, mem_usage, gpu_usage = 0.1, 0.1, 0.1  # 初始化

icon_fav = 'favicon.ico'
icon_cpu = 'icons/cpu.ico'
icon_mem = 'icons/mem.ico'
icon_gpu = 'icons/gpu.ico'
icon_quit = 'icons/quit.ico'

icons_runcat = [f'icons/runcat/{i}.ico' for i in range(5)]
icons_mario = [f'icons/mario/{i}.ico' for i in range(3)]

icon_type = 'runcat'  # 设定默认图标，并加载
icon_list = icons_mario if icon_type == 'mario' else icons_runcat

hover_text = ''


# thread 1: get cpu usage
def thread_get_cpu_usage():
    global cpu_usage, mem_usage, gpu_usage

    while thread_flags:
        cpu_usage = psutil.cpu_percent(interval=1) / 100
        mem_usage = psutil.virtual_memory().percent / 100
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_usage = meminfo.used / meminfo.total
        # print(cpu_usage)
        time.sleep(0.5)


# thread 2: update icon
def thread_update_icon():
    while thread_flags:
        mon = cpu_usage
        if monitor == 'mem':
            mon = mem_usage
        elif monitor == 'gpu':
            mon = gpu_usage

        t = 0.2 - mon * 0.15
        # print(mon, t)
        for i in icon_list:
            tip = f'cpu: {cpu_usage:.2%} \nmem: {mem_usage:.2%} \ngpu: {gpu_usage:.2%}'
            systray.update(icon=i, hover_text=tip)
            # print(i, monitor_type, f'{mon}:.2%')
            time.sleep(t)


def changeIconType(new_icon_type):
    global icon_type, icon_list

    print(icon_type, new_icon_type)
    if new_icon_type != icon_type:
        icon_type = new_icon_type
        icon_list = icons_mario if icon_type == 'mario' else icons_runcat


# change monitor type
def changeMonitor(new_monitor):
    global monitor

    print(monitor, new_monitor)
    if monitor != new_monitor:
        monitor = new_monitor


def quit(systray):
    global thread_flags
    thread_flags = 0

    systray.shutdown()


menu_options = (('cpu', icon_cpu, lambda x: changeMonitor('cpu')),
                ('mem', icon_mem, lambda x: changeMonitor('mem')),
                ('gpu', icon_gpu, lambda x: changeMonitor('gpu')),
                ('runcat', icons_runcat[0], lambda x: changeIconType('runcat')),
                ('mario', icons_mario[0], lambda x: changeIconType('mario')))

systray = SysTrayIcon(icon_fav, hover_text, menu_options, on_quit=quit, default_menu_index=1)
systray.start()

threading.Timer(0.1, thread_get_cpu_usage, []).start()
threading.Timer(0.1, thread_update_icon, []).start()

## pyinstaller --hidden-import pkg_resources --hidden-import infi.systray -w -i favicon.ico runcat-pywin32.py --add-data "icons;icons"
