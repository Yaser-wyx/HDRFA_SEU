import json
from time import sleep

from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class User:
    def __init__(self, userJson):
        self.username = userJson['username']
        self.password = userJson['password']


def login(browser: WebDriver, user: User):
    print("进行用户：{}登录".format(user.username))
    usernameInput = browser.find_element_by_id("username")
    passwordInput = browser.find_element_by_id("password")
    usernameInput.send_keys(user.username)
    passwordInput.send_keys(user.password)
    loginBtn = browser.find_element_by_id("login_submit")
    loginBtn.click()
    try:
        browser.find_element_by_id("welcomeMsg")
        print("用户：{} 登录成功！".format(user.username))
        return True
    except NoSuchElementException:
        print("用户：{} 登录失败，请检查密码和用户名！".format(user.username))
        browser.refresh()
        return False


def fillInForm(browser: WebDriver):
    print("开始填写表单。。。")
    temperatureInput = browser.find_element_by_xpath("//input[@name='fieldSTQKfrtw']")
    temperatureInput.send_keys("36.2")  # 体温数据
    checkBtn = browser.find_element_by_xpath("//input[@name='fieldCNS']")
    checkBtn.click()
    submitBtn = browser.find_element_by_xpath("//li[@class='command_button']")
    submitBtn.click()
    okBtn = browser.find_element_by_xpath("//button[@class='dialog_button default fr']")
    okBtn.click()
    print("表单填写完成！")


def enterForm(browser: WebDriver):
    print("查找表单")
    dailyReportBtn = browser.find_element_by_xpath("//*[@id='pf2581']//td[3]/div/a")
    dailyReportBtn.click()
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    stuDailyRepBtn = browser.find_element_by_xpath("//a[@title='学生健康状况日报']")
    stuDailyRepBtn.click()
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
    quitBtn = browser.find_element_by_xpath("//a[@id='quit']")
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
    try:
        with open(file="./config.json", mode='r', encoding="utf-8") as f:
            configJson = json.load(f)
            return configJson
    except FileNotFoundError:
        print("配置文件丢失！！")
        return None


def getBrowser(browserType, showBrowser, webDriverLocation):
    if browserType == 0:  # 默认开启edge浏览器
        browser = openEdgeBrowser(webDriverLocation, showBrowser)
    else:
        browser = openChromeBrowser(webDriverLocation, showBrowser)
    url = "https://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fmy.nuist.edu.cn%2Findex.portal"
    browser.get(url)
    browser.implicitly_wait(10)
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
                        # 进入表单填报
                        enterForm(browser=browser)
                        # 填写表单
                        fillInForm(browser=browser)
                        # print(usernameInput)
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
                    continue

            if errorUserList:
                print("日报填写失败用户个数：" + str(len(errorUserList)) + "\n")
                for user in errorUserList:
                    print("失败用户：{}\n".format(user.username))
            else:
                print("所有用户日报成功填写完成！")
            browser.quit()

        except KeyError:
            print("配置文件数据有误，请检查！！")
        except WebDriverException:
            print("请填写正确的浏览器驱动路径！")

    print("程序运行结束，3S后退出")
    sleep(3)
