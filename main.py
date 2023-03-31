import random
import time
import requests
from lxml import etree
import os
import demoLogger


# 控制参数：
# Headers参数user_agent:伪装浏览器发送请求，降低被监控到的概率
USER_AGENT_LIST = [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
    'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
]
# DirUrl:爬取的小说目录界面链接
DirUrl = 'https://www.ixuanshu.org/book/1037/'
# DirRegex:小说目录的正则表达式
DirRegexTitle = '//*[@id="info"]/div[1]/ul/li/a/text()'
# DirRegexUrl:获取小说Url的正则表达式
DirRegexUrl = '//*[@id="info"]/div[1]/ul/li/a/@href'
# NovelUrl:爬取的小说具体内容前半部分链接
NovelUrl = 'https://www.ixuanshu.org/book/1037/'
# NovelRegex:小说的正则表达式
NovelRegex = '//*[@id="content1"]/text()'
# LogLevel1:控制台输出日志；LogLevel1:日志文件保存的日志等级。日志级别——目前有INFO和DEBUG
LogLevel1 = "DEBUG"
LogLevel2 = "INFO"
# 内容阶段机制：
Start = 0
End = 0
# FilePath:可以指定我们保存的绝对路径地址
FilePath = 'D:/Novel'
# FolderPath:创建保存小说路径 例:FolderPath = 'novel'
FolderPath = '穿越1630之崛起南美'
# 是否需要完成合并 1为true，0为false
whether_join = 1
# 是否打开合并进度条 1为true，0为false
whether_join_processing = 0
# 超时删掉代理地址
timeout = 5
# 保存的目录名称
desTitles = []
# 保存的每章节小说地址url
urls = []

# 定义日志容器
logPrinter = demoLogger.DemoLogger(LogLevel1, LogLevel2).logger

def get_Headers():
    Header = random.choice(USER_AGENT_LIST)
    Headers = {
        'user-agent': Header}
    return Headers


# 预置条件
def open_cmd():
    os.chdir("proxy_pool-2.4.1")
    os.system(' start cmd.exe /K python proxyPool.py server ')
    # 确保代理池完全打开
    time.sleep(3)
    os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))


# 1、判断是否要创建一个目录用来保存下载的txt文件
def judge_folder_if_exist(file_path, folder_path):
    if file_path:
        if not os.path.exists(file_path + "/" + folder_path):
            logPrinter.info("********** Ⅰ 文件夹不存在，申请自动创建路径 **********")
            os.makedirs(file_path + "/" + folder_path)
            os.makedirs(file_path + "/" + folder_path + '/dir')
            os.makedirs(file_path + "/" + folder_path + '/novel')
            logPrinter.info("********** 创建路径完成 **********\n\n")
        else:
            logPrinter.info("********** Ⅰ 文件夹已存在，无需创建 **********\n\n")
    else:
        global FilePath
        FilePath = os.getcwd()
        judge_folder_if_exist(FilePath, folder_path)


def illegal_char_analysis(title):
    for i, j in ("/／", "\\＼", "?？", "|︱", "\"＂", "*＊", "<＜", ">＞"):
        title = title.replace(i, j)
    return title

# 2、读取一级目录界面，将目录数据和小说每一章节URL保存在dir文件夹下
def get_dir(url, dirRegexTitle, dirRegexUrl):
    # 请求获取目录
    logPrinter.info("********** Ⅱ 正在请求生成 目录.txt 和 URL.txt 文件...... **********")
    response = requests.get(url, headers=get_Headers())
    response.encoding = 'utf-8'
    selector = etree.HTML(response.text)
    srcTitles = selector.xpath(dirRegexTitle)
    os.chdir(FilePath + "/" + FolderPath + '/dir')
    # 生成目录文件
    for title in srcTitles:
        temp = title.replace('\n', '').replace('\r', '').strip()
        temp = illegal_char_analysis(temp)
        desTitles.append(temp)
    del desTitles[Start: End]
    with open("目录.txt", "w", encoding="utf-8") as f:
        for i in range(len(desTitles)):
            f.write(desTitles[i] + '\n')
    # 生成URL文件
    hrefs = selector.xpath(dirRegexUrl)
    del hrefs[Start: End]
    for href in hrefs:
        urls.append(NovelUrl + href)
    with open("URL.txt", "w", encoding="utf-8") as f:
        for i in range(len(urls)):
            f.write(urls[i] + '\n')
    print("目录信息：", desTitles)
    print("URL信息：", urls)
    logPrinter.info("********** 目录和URL生成完毕 **********\n\n")


def if_txt_not_null(txt):
    if not os.path.getsize(txt):
        return 0
    return 1
# 从ip池中申请ip
def get_proxy():
    data = requests.get("http://127.0.0.1:5010/get/").json()
    logPrinter.debug("成功获取代理地址: %a", data.get("proxy"))
    return data
# 删除掉不可以使用的ip
def delete_proxy(proxy):
    logPrinter.error("错误！正在删除错误代理地址: %s", proxy)
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# 3、读取小说界面，保存数据到novel文件夹下
def get_novel(novelRegex):
    logPrinter.info("********** Ⅲ 正在请求下载小说 **********")
    os.chdir(FilePath + '/' + FolderPath + '/novel')
    i = 0
    while i < len(urls):
        if os.path.exists(desTitles[i] + ".txt") and if_txt_not_null(desTitles[i] + ".txt"):
            i += 1
            continue
        # time.sleep(0.3)
        proxy = get_proxy().get("proxy")
        try:
            # 使用代理访问=
            response = requests.get(urls[i], headers=get_Headers(), proxies={"http": "http://{}".format(proxy)},
                                    timeout=timeout)
            response.encoding = 'utf-8'
            selector = etree.HTML(response.text)
            contents = selector.xpath(novelRegex)
            if not contents:
                logPrinter.info(desTitles[i] + "的返回值为空，重新下载")
                time.sleep(5)
                continue
            with open(desTitles[i] + ".txt", "w", encoding="utf-8") as f:
                for j in range(len(contents)):
                    # if j == 0:
                    #     continue
                    content = '    ' + contents[j].replace('\n', '').strip() + '\n'
                    f.write(content)
            temp = round(((i + 1) / len(urls) * 100), 2)
            process = str(temp) + '%'
            logPrinter.debug("当前下载进度: " + process)
            logPrinter.info(str(desTitles[i]) + "下载成功！\n")
        except Exception as ex:
            # # 删除代理池中代理
            # delete_proxy(proxy)
            i -= 1
            logPrinter.error(str(desTitles[i]) + "下载失败！")
            logPrinter.error("出现如下报错信息：%s", ex)
            print(ex.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(ex.__traceback__.tb_lineno)  # 发生异常所在的行数
    logPrinter.info("********** 下载完毕 **********\n\n")
    return 1


# 可以生成不同格式的结果文件
def file_generation(file_format):
    i = 0
    f = open(FilePath + '/' + FolderPath + "/dir/目录.txt", encoding='utf-8')
    line = f.readline()
    os.chdir(FilePath + '/' + FolderPath)
    with open(FolderPath + file_format, "w", encoding="utf-8") as fa:
        os.chdir(FilePath + '/' + FolderPath + '/novel')
        while line:
            # 合并进度条
            if whether_join_processing:
                temp0 = round(((i + 1) / len(urls) * 100), 2)
                process = str(temp0) + "%"
                temp = int((i + 1) / len(urls) * 100)
                msg = "|"
                for j in range(temp):
                    msg += '▇'
                for j in range(100 - temp):
                    msg += ' '
                msg += "|"
                print('\r' + "当前合并进度(" + file_format + "文档): " + msg + process, end='')
                i += 1
            # 写入文件
            f1 = open(line.replace('\n', '') + '.txt', encoding='utf-8')
            fa.write(line)
            line1 = f1.readline()
            while line1:
                fa.write(line1)
                line1 = f1.readline()
            f1.close()
            fa.write('\n\n')
            line = f.readline()
    f.close()
    if whether_join_processing:
        print("")

# 4、合并结果
def join():
    logPrinter.info("********** Ⅳ 合并小说每一章节 **********")
    file_generation(".txt")
    file_generation(".md")
    logPrinter.info("********** 合并完成 **********\n\n\n\n")


if __name__ == '__main__':
    # 预置条件
    # open_cmd()
    # 1、判断是否存在novel文件夹，用来后续存放下载的小说
    judge_folder_if_exist(FilePath, FolderPath)
    # 2、获取小说目录，并保存到txt文件中
    get_dir(DirUrl, DirRegexTitle, DirRegexUrl)
    # 3、读取小说内容，并保存到novel文件夹中
    result = get_novel(NovelRegex)
    # 4、合并下载的文件？
    if whether_join and result:
        join()
