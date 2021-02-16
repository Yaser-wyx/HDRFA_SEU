import datetime
import os


def isNewDay():
    print("检查是否是新的一天。。。")
    try:
        with open(os.getcwd() + "\\task.log", 'r', encoding='utf-8') as f:
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
    os.system(os.getcwd() + "\\main.exe")
    with open(os.getcwd() + "\\task.log", mode='a', encoding='utf-8') as f:
        f.write("\n" + str(datetime.date.today()) + " | 任务执行！\n")


if __name__ == '__main__':
    if isNewDay():
        print("是新的一天，开始运行程序")
        job()
    else:
        print("不是新的一天。。")
    print("程序结束。。。")
