import threading
import time

import psutil
import pystray

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
    global cpu_usage
    while True:
        cpu_usage = psutil.cpu_percent(interval=1) / 100
        time.sleep(0.5)


cpu_usage = 0.2  # 初始化
cats =  [ICOImage(f'icons/runcat/{i}.ico') for i in range(5)]
runcat = pystray.Icon('run cat', icon=cats[0])





# starts the setup thread.
def start_setup(setup):
    runcat.visible = True
    threading.Thread(target=thread_get_usage).start()
    
    while True:
        for icon in cats:
            runcat.icon = icon
            mon = cpu_usage
            t = 0.2 - mon * 0.15
            print(f'{mon=:.2%}, {t=:.2f}s, {cpu_usage=:.2%}')
   
            time.sleep(t)


runcat.run(setup=start_setup)

