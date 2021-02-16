import os

import psutil

if __name__ == '__main__':
    TARGET_NAME = "task.exe"
    flag = False
    for proc in psutil.process_iter():
        if proc.name().lower() == TARGET_NAME:
            print("找到task进程！")
            flag = True
            break

    if flag:
        cmd = 'taskkill /F /IM ' + TARGET_NAME
        os.system(cmd)
        print("task进程关闭成功")
    else:
        print("没有task进程哦！")

    os.system('pause')
