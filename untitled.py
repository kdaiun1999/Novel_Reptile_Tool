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
import logging

import os

root_dir = os.getcwd()
log_dir = os.path.join(root_dir, "logs")

if not os.path.exists(log_dir):
    os.mkdir(log_dir)


class DemoLogger:
    def __init__(self):
        # 创建一个日志器
        self.logger = logging.getLogger("logger")

        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(logging.INFO)

        # 创建处理器：sh为控制台处理器，fh为文件处理器
        sh = logging.StreamHandler()

        # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
        # log_file = os.path.join(log_dir,"{}_log".format(time.strftime("%Y/%m/%d",time.localtime())))
        log_file = os.path.join(log_dir, "autotest.log")
        fh = logging.FileHandler(log_file, encoding="UTF-8")

        # 创建格式器,并将sh，fh设置对应的格式
        formatter = logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(message)s",
                                      datefmt="%Y/%m/%d %X")
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 将处理器，添加至日志器中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


logPrinter = DemoLogger().logger
if __name__ == '__main__':
    logPrinter.debug("------这是debug信息---")
    logPrinter.info("------这是info信息---")
    logPrinter.warning("------这是warning信息---")
    logPrinter.error("------这是error信息---")
    logPrinter.critical("------这是critical信息---")
