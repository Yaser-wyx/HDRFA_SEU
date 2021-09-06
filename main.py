# utf-8
import datetime
import json
import os
from time import sleep

from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import ActionChains

errorFlag = False


class User:
    def __init__(self, userJson):
        self.username = userJson['username']
        self.password = userJson['password']


def login(browser: WebDriver, user: User):
    print("进行用户：{}登录".format(user.username))
    login_btn = browser.find_element_by_id("ampHasNoLogin")
    login_btn.click()
    usernameInput = browser.find_element_by_id("username")
    passwordInput = browser.find_element_by_id("password")
    usernameInput.click()
    usernameInput.send_keys(user.username)
    passwordInput.click()
    passwordInput.send_keys(user.password)
    loginBtn = browser.find_element_by_id("xsfw")
    loginBtn.click()
    sleep(1)

    def login_fail(user):
        global errorFlag
        print("用户：{} 登录失败，请检查密码和用户名！".format(user.username))
        browser.refresh()
        errorFlag = True
        return False

    try:
        user_id = browser.find_element_by_xpath(
            "//*[@id=\"app\"]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/div/a/div[3]").text[-9:]
        print(user_id)
        if user_id == user.username:
            print("用户：{} 登录成功！".format(user.username))
            return True
        else:
            return login_fail(user)
    except NoSuchElementException:
        return login_fail(user)


def fillInForm(browser: WebDriver):
    print("开始填写表单。。。")
    sleep(1)
    addNewBtn = browser.find_element_by_xpath("/html/body/main/article/section/div[2]/div[1]")
    addNewBtn.click()
    sleep(3)
    try:
        temperatureInput = browser.find_element_by_xpath(
            "/html/body/div[11]/div/div[1]/section/div[2]/div/div[4]/div[2]/div[1]/div/div/input")
        temperatureInput.send_keys("36.2")  # 体温数据
        saveBtn = browser.find_element_by_xpath("//*[@id=\"save\"]")
        saveBtn.click()
        okBtn = browser.find_element_by_xpath("/html/body/div[62]/div[1]/div[1]/div[2]/div[2]/a[1]")
        okBtn.click()
    except NoSuchElementException:
        hasFilled = browser.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[2]/div[1]/div").text
        if hasFilled == "今日已填报！":
            print("今天的日报已经填过啦！")

    print("表单填写完成！")


def enterForm(browser: WebDriver):
    print("查找表单")

    serverBtn = browser.find_element_by_xpath("//*[@id=\"app\"]/div[2]/div[1]/div/div[2]/div/a[2]")
    serverBtn.click()
    sleep(1)
    searchInput = browser.find_element_by_xpath("//*[@id=\"app\"]/div[2]/div[2]/div/div/div/div[1]/div[3]/input")
    searchInput.send_keys("全校师生每日健康申报系统")
    sleep(1)
    searchInput.send_keys(Keys.ENTER)
    sleep(1)
    entranceBtn = browser.find_element_by_xpath("//*[@id=\"app\"]/div[2]/div[2]/div/div/div/div[3]/div/div[2]/a")
    entranceBtn.click()
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    print("进入表单成功！")


def exitUser(browser: WebDriver):
    print("退出当前用户")
    windows = browser.window_handles
    for window in windows[1:]:
        # 关闭除第一个窗口外的其它窗口
        browser.switch_to.window(window)
        browser.close()
    browser.switch_to.window(windows[0])
    userBtn = browser.find_element_by_xpath("//*[@id=\"app\"]/div[2]/div[1]/div/div[3]/span/div")
    ActionChains(driver=browser).move_to_element(userBtn).perform()
    sleep(0.5)
    quitBtn = browser.find_element_by_xpath("//*[@id=\"app\"]/div[2]/div[1]/div/div[3]/span/div/div/a[2]")
    quitBtn.click()
    print("当前用户退出成功！")


def openEdgeBrowser(webDriverLocation: str, showBrowser: bool) -> webdriver:
    print("打开Edge浏览器！")
    option = EdgeOptions()
    # 开启无头模式.
    if not showBrowser:
        option.use_chromium = True
        option.headless = True
    browser = Edge(executable_path=webDriverLocation, options=option)
    return browser


def openChromeBrowser(webDriverLocation: str, showBrowser: bool) -> webdriver:
    print("打开chrome浏览器！")
    option = Options()
    # 开启无头模式.
    if not showBrowser:
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        option.add_argument("--blink-settings=imagesEnabled=false")
    chromeBrowser = webdriver.Chrome(executable_path=webDriverLocation, options=option)
    return chromeBrowser


def loadConfig():
    global errorFlag

    try:
        with open(file="./config.json", mode='r', encoding="utf-8") as f:
            configJson = json.load(f)
            return configJson
    except FileNotFoundError:
        print("配置文件丢失！！")
        errorFlag = True
        return None


def getBrowser(browserType, showBrowser, webDriverLocation):
    if browserType == 0:  # 默认开启edge浏览器
        browser = openEdgeBrowser(webDriverLocation, showBrowser)
    else:
        browser = openChromeBrowser(webDriverLocation, showBrowser)
    url = "http://ehall.seu.edu.cn/new/index.html"
    browser.get(url)
    browser.implicitly_wait(8)
    return browser


if __name__ == '__main__':
    errorUserList = []
    config = loadConfig()
    if config:
        try:
            userJsonList = config['userList']
            webDriverLocation = config['webDriverLocation']  # 浏览器驱动路径
            browserType = config['browserType']
            showBrowser = config['showBrowser']
            userList = []
            for userJson in userJsonList:
                userList.append(User(userJson))  # 将json转为user对象
            browser = getBrowser(browserType=browserType, showBrowser=showBrowser, webDriverLocation=webDriverLocation)
            for user in userList:
                try:
                    # 登录
                    if login(browser=browser, user=user):
                        pass
                        # 进入表单填报
                        enterForm(browser=browser)
                        # 填写表单
                        fillInForm(browser=browser)
                        print("用户：{} 日报填写完成！".format(user.username))
                        # 退出当前用户
                        exitUser(browser=browser)
                except Exception as ex:
                    print("用户：{}日报填写出现异常！请自行检查！！\n".format(user.username))
                    print("异常信息：{}".format(ex))
                    errorUserList.append(user)
                    # 异常恢复
                    print("开始恢复异常，重启浏览器。。。")
                    browser.quit()
                    browser = getBrowser(browserType=browserType, showBrowser=showBrowser,
                                         webDriverLocation=webDriverLocation)
                    errorFlag = True
                    continue

            if errorUserList:
                print("日报填写失败用户个数：" + str(len(errorUserList)) + "\n")
                for user in errorUserList:
                    print("失败用户：{}\n".format(user.username))
            else:
                print("所有用户日报成功填写完成！")
            browser.quit()

        except KeyError:
            errorFlag = True
            print("配置文件数据有误，请检查！！")
        except WebDriverException:
            errorFlag = True
            print("请填写正确的浏览器驱动路径！")
    if errorFlag:
        msg = "\n" + str(datetime.date.today()) + " | 任务执行 | Fail"
    else:
        msg = "\n" + str(datetime.date.today()) + " | 任务执行 | Success"
    # 写入运行日志
    with open(os.getcwd() + "\\task.log", mode='a', encoding='utf-8') as f:
        f.write(msg)
    print("程序运行结束，3S后退出")
    sleep(3)
