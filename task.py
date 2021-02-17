import datetime
import os
import sys
from time import sleep


def isNewDay(logMsg: str):
    print("检查是否是新的一天。。。")
    if logMsg:
        try:
            timeStr = logMsg.split("|")[0].strip()
            time = datetime.datetime.strptime(timeStr, '%Y-%m-%d')
            timeDelta = (datetime.datetime.today() - time).days
            return timeDelta >= 1
        except Exception:
            print("task.log文件数据异常，请清空数据或删除该文件后重启程序。。")
            sleep(3)
            print("程序退出。。。")
            sys.exit()
    return True  # 如果文件没有内容或者天数大于1，则返回True


def getNewestLog():
    try:
        with open(os.getcwd() + "\\task.log", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                filteredLines = []
                for line in lines:
                    if len(line) > 0:
                        filteredLines.append(line)
                if len(filteredLines) > 0:
                    return filteredLines[-1]
            return None  # 如果没有数据
    except FileNotFoundError:
        return None


def preTaskIsSuccess(logMsg: str):
    print("检查上一次任务是否成功。。")
    if logMsg:
        try:
            preTaskStatus = logMsg.split("|")[-1].strip()
            return preTaskStatus != "Fail"
        except Exception:
            print("task.log文件数据异常，请清空数据或删除该文件后重启程序。。")
            sleep(3)
            print("程序退出。。。")
            sys.exit()
    return False


if __name__ == '__main__':
    logMsg = getNewestLog()
    if isNewDay(logMsg) or not preTaskIsSuccess(logMsg):
        print("上一次任务失败，或者是新的一天了，开始运行程序")
        os.system(os.getcwd() + "\\main.exe")
    else:
        print("上一次任务运行成功。。")

    print("程序运行结束，即将退出。。。")
    sleep(3)
