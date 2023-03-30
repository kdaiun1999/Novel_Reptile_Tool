#
#
#
# def funA(fn):
#     print("testA start")
#     fn()
#     print("TestA end!")
#     # return 0
#
# @funA
# def funB():
#     """ProxyPool cli工具"""
#     print("testB start")
#     print("TestB end！")
#
# if __name__ == '__main__':
#     # funA(fn)
#
#     print('\n')
#
#     funB()

# from handler.logHandler import LogHandler
# import logging
#
# logging.basicConfig(level=logging.DEBUG  # 设置日志输出格式
#                     , filename="demo.log"  # log日志输出的文件位置和文件名
#                     , filemode="a"  # 文件的写入格式，w为重新写入文件，默认是追加
#                     , format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
#                     # 日志输出的格式
#                     # -8表示占位符，让输出左对齐，输出长度都为8位
#                     , datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
#                     )
#
# logging.debug("This is  DEBUG !!")
# logging.info("This is  INFO !!")
# logging.warning("This is  WARNING !!")
# logging.error("This is  ERROR !!")
# logging.critical("This is  CRITICAL !!")
# logging.info("true")

# Time:2022 2022/3/2 10:21
# Author: Jasmay
# -*- coding: utf-8 -*-

# 定义日志容器
import time
import requests
from lxml import etree
import os
import demoLogger


Headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                  'Safari/537.36'}
# DirUrl:爬取的小说目录界面链接
DirUrl = 'https://www.biquge365.net/newbook/45173/'
# NovelUrl:爬取的小说具体内容前半部分链接
NovelUrl = 'https://www.biquge365.net/chapter/45173/30090551.html'
# FilePath:可以指定我们保存的绝对路径地址
FilePath = 'D:/Novel'
# FolderPath:创建保存小说路径 例:FolderPath = 'novel'
FolderPath = '寒门败家子'

logPrinter = demoLogger.DemoLogger().logger
def get_dir(url, url1):
    # 请求获取目录
    logPrinter.info("********** Ⅱ 正在请求生成 目录.txt 和 URL.txt 文件...... **********")
    response = requests.get(url, headers=Headers)
    response.encoding = 'utf-8'
    selector = etree.HTML(response.text)
    srcTitles = selector.xpath('')
    logPrinter.info(srcTitles)

    time.sleep(1)
    response = requests.get(url1, headers=Headers)
    response.encoding = 'utf-8'
    selector = etree.HTML(response.text)
    srcTitles = selector.xpath('// *[ @ id = "txt"] / text()')
    logPrinter.info(srcTitles)



if __name__ == '__main__':
    get_dir(DirUrl, NovelUrl)






    # logPrinter.info(os.getcwd())
    # os.chdir(FilePath + "/" + FolderPath + '/dir')
    # # 生成目录文件
    # for title in srcTitles:
    #     temp = title.replace('\n', '').replace('\r', '').strip()
    #     desTitles.append(temp)
    # del desTitles[0: 12]
    # with open("目录.txt", "w", encoding="utf-8") as f:
    #     for i in range(len(desTitles)):
    #         f.write(desTitles[i] + '\n')
    # # 生成URL文件
    # hrefs = selector.xpath('//*[@id="list"]/dl/dd/a/@href')
    # del hrefs[0: 12]
    # for href in hrefs:
    #     urls.append(NovelUrl + href)
    # with open("URL.txt", "w", encoding="utf-8") as f:
    #     for i in range(len(urls)):
    #         f.write(urls[i] + '\n')
    # logPrinter.info("目录信息：%a", desTitles)
    # logPrinter.info("URL信息：%a", urls)
    # logPrinter.info("********** 目录和URL生成完毕 **********\n\n")

