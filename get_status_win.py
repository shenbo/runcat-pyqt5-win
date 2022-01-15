import psutil
import pynvml

# cpu
cpu_usage = psutil.cpu_percent(interval=1) / 100

# memory
mem_total = psutil.virtual_memory().total
mem_usage = psutil.virtual_memory().percent / 100

# gpu
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)   # GPU id: 0
gpu_mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
gpu_total = gpu_mem.total
gpu_usage = gpu_mem.used / gpu_mem.total
gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, 0)
gpu_fan = pynvml.nvmlDeviceGetFanSpeed(handle)
# gpu_power = pynvml.nvmlDeviceGetPowerUsage(handle)

# ip
def get_ip():
    net_info = psutil.net_if_addrs()
    for k, v in net_info.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                ip_addr = item[1]
                return ip_addr

ip_addr = get_ip()

###
status = 'Win10 Status: \n'
status += f'```\n'
status += f'CPU Used  = {cpu_usage:.2%} \n'
status += f'RAM Total = {mem_total/1e9:.2f} G \n'
status += f'RAM Used  = {mem_usage:.2%} \n'
status += f'GPU Total = {gpu_total/1e9:.2f} G \n'
status += f'GPU Used  = {gpu_usage:.2%} \n'
status += f'GPU Temp  = {gpu_temp} °C \n'
status += f'GPU FanSp = {gpu_fan}% \n'
# status += f'GPU Power = {gpu_power} W \n'
status += f'IP  Addr  = {ip_addr} \n'
status += '```'
print(status)
