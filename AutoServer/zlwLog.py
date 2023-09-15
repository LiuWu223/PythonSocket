import os.path
import time
import sys
import zlwTool.zlwLog.loggingG as loggingG
"""
文件名称：日志格式化封装
创建时间：2023_03_23
"""
"""日志命名时间格式化"""


def thisTime():
    times = time.time()
    localtime = time.localtime(times)
    year = localtime.tm_year
    mon = localtime.tm_mon
    mday = localtime.tm_mday
    hour = localtime.tm_hour
    mins = localtime.tm_min
    if int(mon) < 10:
        mon = "0" + str(mon)
    if int(mday) < 10:
        mday = "0" + str(mday)
    if int(hour) < 10:
        hour = "0" + str(hour)
    if int(mins) < 10:
        mins = "0" + str(mins)
    retTime = str(year) + str(mon) + str(mday) + str(hour) + str(mins)
    return retTime


"""日志格式化"""


def logging_setting(**kwargs):
    """
    格式日志
    可传参数为：logName: 自定义日志命名（默认以当前文件路径命名）
    logPath: 自定义.log保存路径(默认在当前执行文件目录下创建log文件夹，里面存放.log)
    :return: log
    """
    # 默认日志名为当前执行的文件名
    logName = sys.argv[0]
    # 当前执行文件夹
    logPath = os.getcwd().replace("/", "\\")
    for key,value in kwargs.items():
        if key == "logName":
            # 发现logName参数，把日志名设置为当前执行文件名+传过来的参数
            logName = sys.argv[0] + ", User >> " + value
        if key == "logPath":
            logPath = value

    log = loggingG.getLogger(logName)
    # 设置日志记录器的级别 DEBUG数值最小 所以所有登记的LOG都能看到
    log.setLevel(loggingG.DEBUG)

    # ======================输出至控制台
    hander1 = loggingG.StreamHandler()  # stream=sys.stdout 输出至控制台
    hander1.setLevel(loggingG.DEBUG)
    formatter1 = loggingG.Formatter("%(asctime)s %(levelname)s [%(name)s]: %(message)s")
    hander1.setFormatter(formatter1)

    try:
        if not os.path.exists(logPath + "\log"):
            # 创建文件夹
            os.mkdir(logPath + "\log")
    except FileNotFoundError as err:
        print(str(err)+", 默认输入至工作目录下")
        logPath = os.getcwd().replace("/", "\\")
        if not os.path.exists(logPath + "\log"):
            # 创建文件夹
            os.mkdir(logPath + "\log")

    # ======================输出.log
    hander2 = loggingG.FileHandler(logPath + '\log\{}.log'.format(thisTime()), mode='w', encoding='utf-8')

    # 日志可接收等级
    hander2.setLevel(loggingG.DEBUG)
    formatter2 = loggingG.Formatter("%(asctime)s %(levelname)s [%(name)s]: %(message)s")
    hander2.setFormatter(formatter2)

    # 将日志处理器和日志记录器组合起来
    log.addHandler(hander1)
    log.addHandler(hander2)
    return log


if __name__ == "__main__":
    pass
