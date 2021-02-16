import datetime
import os
from time import sleep


def isNewDay():
    try:
        with open("task.log", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 0:
                lastLine = lines[-1]
                timeStr = lastLine.split("|")[0].strip()
                time = datetime.datetime.strptime(timeStr, '%Y-%m-%d')
                timeDelta = (datetime.datetime.today() - time).days
                if timeDelta < 1:
                    # 不是新的一天
                    return False
            return True  # 如果文件没有内容或者天数大于1，则返回True
    except FileNotFoundError:
        return True


def job():
    os.system("main.exe")
    with open('task.log', mode='a', encoding='utf-8') as f:
        f.write(str(datetime.date.today()) + " | 任务执行！\n")


if __name__ == '__main__':
    try:
        while True:
            if isNewDay():
                job()
            sleep(3600)  # 每小时检查一次
    except Exception as ex:
        with open('error.txt', 'a', encoding='utf-8') as f:
            f.write(str(ex))
