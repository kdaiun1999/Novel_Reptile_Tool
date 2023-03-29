# Novel_Reptile_Tool
笔趣阁爬虫小工具使用了免费的代理

# 用到了免费代理池（原理也是从别的免费代理网站上爬取可用代理ip，存放在本地redis中）
首先需要打开proxy_pool-2.4.1文件夹，执行cmd，运行命令行如下：
>> python proxyPool.py schedule
这一步需要等到代理地址都加载进入代理池后关闭


pycharm打开文件夹，运行main函数开始执行下载
