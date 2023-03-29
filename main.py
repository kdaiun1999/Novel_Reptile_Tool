import time
import requests
from lxml import etree
import os
import demoLogger


# 定义日志容器
logPrinter = demoLogger.DemoLogger().logger

# 控制参数：
# Headers:伪装浏览器发送请求，降低被监控到的概率
Headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36'}
# DirUrl:爬取的小说目录界面链接
DirUrl = 'http://www.42zw.la/book/32451/'
# NovelUrl:爬取的小说具体内容前半部分链接
NovelUrl = 'http://www.42zw.la'
# FilePath:可以指定我们保存的绝对路径地址
FilePath = 'D:/Novel'
# FolderPath:创建保存小说路径 例:FolderPath = 'novel'
FolderPath = '寒门败家子'
# 是否需要完成合并 1为true，0为false
whether_join = 1
# 超时删掉代理地址
timeout = 5
# 保存的目录名称
desTitles = []
# 保存的每章节小说地址url
urls = []


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
            logPrinter.info("********** 创建路径完成 **********\n")
        else:
            logPrinter.info("********** Ⅰ 文件夹已存在，无需创建 **********\n")
    else:
        global FilePath
        FilePath = os.getcwd()
        judge_folder_if_exist(FilePath, folder_path)


# 2、读取一级目录界面，将目录数据和小说每一章节URL保存在dir文件夹下
def get_dir(url):
    # 请求获取目录
    logPrinter.info("********** Ⅱ 正在请求生成 目录.txt 和 URL.txt 文件...... **********")
    response = requests.get(url, headers=Headers)
    response.encoding = 'utf-8'
    selector = etree.HTML(response.text)
    srcTitles = selector.xpath('//*[@id="list"]/dl/dd/a/text()')
    logPrinter.info(os.getcwd())
    os.chdir(FilePath + "/" + FolderPath + '/dir')
    # 生成目录文件
    for title in srcTitles:
        temp = title.replace('\n', '').replace('\r', '').strip()
        desTitles.append(temp)
    del desTitles[0: 12]
    with open("目录.txt", "w", encoding="utf-8") as f:
        for i in range(len(desTitles)):
            f.write(desTitles[i] + '\n')
    # 生成URL文件
    hrefs = selector.xpath('//*[@id="list"]/dl/dd/a/@href')
    del hrefs[0: 12]
    for href in hrefs:
        urls.append(NovelUrl + href)
    with open("URL.txt", "w", encoding="utf-8") as f:
        for i in range(len(urls)):
            f.write(urls[i] + '\n')
    logPrinter.info("目录信息：%a", desTitles)
    logPrinter.info("URL信息：%a", urls)
    logPrinter.info("********** 目录和URL生成完毕 **********\n")


def if_txt_not_null(txt):
    if not os.path.getsize(txt):
        return 0
    return 1
# 从ip池中申请ip
def get_proxy():
    data = requests.get("http://127.0.0.1:5010/get/").json()
    logPrinter.info("成功获取代理地址: %a", data.get("proxy"))
    return data
# 删除掉不可以使用的ip
def delete_proxy(proxy):
    logPrinter.info("错误！正在删除错误代理地址: %s", proxy)
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# 3、读取小说界面，保存数据到novel文件夹下
def get_novel():
    logPrinter.info("********** Ⅲ 正在请求下载小说 **********")
    os.chdir(FilePath + '/' + FolderPath + '/novel')
    i = 0
    while i < len(urls):
        if os.path.exists(desTitles[i] + ".txt") and if_txt_not_null(desTitles[i] + ".txt"):
            i += 1
            continue
        time.sleep(0.3)
        proxy = get_proxy().get("proxy")
        try:
            # 使用代理访问
            response = requests.get(urls[i], headers=Headers, proxies={"http": "http://{}".format(proxy)},
                                    timeout=timeout)
            response.encoding = 'utf-8'
            # logPrinter.info("url = ", urls[i])
            # logPrinter.info(response)
            selector = etree.HTML(response.text)
            contents = selector.xpath('//*[@id="content"]/p/text()')
            # logPrinter.info(contents)
            if not contents:
                logPrinter.info(desTitles[i] + "的返回值为空，重新下载")
                continue
            with open(desTitles[i] + ".txt", "w", encoding="utf-8") as f:
                for j in range(len(contents)):
                    if j == 0 or j == 1:
                        continue
                    content = '    ' + contents[j].replace('\n', '').strip() + '\n'
                    f.write(content)
            logPrinter.info(str(desTitles[i]) + "下载成功！\n")
        except Exception as ex:
            # # 删除代理池中代理
            delete_proxy(proxy)
            i -= 1
            logPrinter.info(str(desTitles[i]) + "下载失败！")
            logPrinter.info("出现如下报错信息：%s", ex)
    logPrinter.info("********** 下载完毕 **********\n")
    return 1


# 4、合并结果
def join():
    logPrinter.info("********** Ⅳ 合并小说每一章节 **********")
    logPrinter.info(os.getcwd())
    f = open(FilePath + '/' + FolderPath + "/dir/目录.txt", encoding='utf-8')
    line = f.readline()
    os.chdir(FilePath + '/' + FolderPath)
    with open("寒门败家子.txt", "w", encoding="utf-8") as fa:
        os.chdir(FilePath + '/' + FolderPath + '/novel')
        while line:
            f1 = open(line.replace('\n', '') + '.txt', encoding='utf-8')
            line1 = f1.readline()
            while line1:
                fa.write(line1)
                line1 = f1.readline()
            f1.close()
            fa.write('\n\n')
            line = f.readline()
    f.close()
    logPrinter.info("********** 合并完成 **********")


if __name__ == '__main__':
    # 预置条件
    open_cmd()
    # 1、判断是否存在novel文件夹，用来后续存放下载的小说
    judge_folder_if_exist(FilePath, FolderPath)
    # 2、获取小说目录，并保存到txt文件中
    get_dir(DirUrl)
    # 3、读取小说内容，并保存到novel文件夹中
    result = get_novel()
    # 4、合并下载的文件？
    if whether_join and result:
        join()
