import os

import win32api
import win32con


def register():
    print("注册开机启动项")
    fileName = os.path.basename("task.exe")
    name = os.path.splitext(fileName)[0]
    path = os.path.abspath(os.path.dirname(__file__)) + '\\' + fileName
    # 注册表项名
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    # 异常处理
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(key)
    except Exception:
        print('添加开机启动项失败...')
    print('添加开机启动项成功！')


if __name__ == '__main__':
    # 开机启动注册有问题
    register()
    os.system("start task.exe")
    os.system('pause')
