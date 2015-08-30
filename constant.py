# coding:UTF-8
__author__ = 'key'
import re

WEB_RE = r'[a-zA-z]+://[^\s\（\）\(\)\(\)]*'  # 网址的正则表达式
TAG_RE = r'#[^#]*#'  # tag的正则表达式
USER_RE = r'\@[^@]*'
URL_PATT = re.compile(WEB_RE)
TAG_PATT = re.compile(TAG_RE)
USER_PATT = re.compile(USER_RE)
STA_DAY = 7  # 统计多少天内的平均数
RF_NUMBER = 3  # 随机森林数量
MAX_DEPTH = 100  #随机森林最深层数
