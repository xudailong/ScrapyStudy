# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 10:48
# @Author  : 蛇崽
# @Email   : 643435675@QQ.com
# @File    : Main.py
from scrapy.cmdline import execute
import sys
import os


# 这个文件只是一个命令，进行执行scrapy命令操作
targetLine = 'quweiji'
execute(['scrapy', 'crawl', targetLine])