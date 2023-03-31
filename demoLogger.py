import logging

import os

root_dir = os.getcwd()
log_dir = os.path.join(root_dir, "logs")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)


class DemoLogger:
    def __init__(self, type1, type2):
        # 创建一个日志器
        self.logger = logging.getLogger("logger")
        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(logging.DEBUG)

        # 创建处理器：sh为控制台处理器，fh为文件处理器
        sh = logging.StreamHandler()
        sh.setLevel(type1)

        # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
        # log_file = os.path.join(log_dir,"{}_log".format(time.strftime("%Y/%m/%d",time.localtime())))
        log_file = os.path.join(log_dir, "logs.log")
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(type2)

        # 创建格式器,并将sh，fh设置对应的格式
        formatter = logging.Formatter("%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - "
                                      "%(message)s", "%Y-%m-%d %H:%M:%S")
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 将处理器，添加至日志器中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
