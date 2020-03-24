# runcat-pyqt5-win

[RunCat](http://kyomesuke.com/runcat/index.html) 是一款 mac应用，用奔跑的猫来显示当前系统资源（CPU）占用情况。

但是只有mac版，于是用python撸了一个，可以在windows任务栏（通知区域）养猫。

首先用[psutil](https://pypi.org/project/psutil/)
获得CPU或内存的使用情况，然后用pyqt5创建QSystemTrayIcon显示在任务栏的托盘区域。

GPU使用情况可以用[nvidia-ml-py](https://pypi.org/project/nvidia-ml-py/)
的pynvml模块（仅限nvidia gpu）。

## Screenshot

![](runcat-screenshot.gif)

## Requirements
- psutil
- pyqt5
- nvidia-ml-py

## Usage

- 直接clone， 改 *.pyw 运行

- ~~或者下载打包后的程序[下载7z](https://github.com/shenbo/runcat-pyqt5-win/releases)~~  

> ref:
> - https://github.com/Kyome22/menubar_runcat
> - https://github.com/sunthx/RunCat-Win


## Versions

V0.2
- add context menu
  - change icon type
  - quit 
- add mario icons

V0.1 
- runcat @ cpu 
- runcat @ memory 
- runcat @ gpu
