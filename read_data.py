# coding:UTF-8
__author__ = 'key'
from  datetime import *
from constant import *


def read_train_data(*par):
    temp = par[0] if len(par) > 0 else None
    file_in = open("weibo_train_data.txt")
    weibo_list = []
    for line in file_in.readlines()[:temp]:
        # print line
        line_spl = line.split()
        content = (' ').join(line_spl[6:])  # 提取内容
        url_find = URL_PATT.findall(content)  # 包含的url的列表；
        tag_find = TAG_PATT.findall(content)  # 包含的tag的列表；
        line_spl = line_spl[0:6] + [content]
        line_spl = (
            line_spl[0], line_spl[1], datetime.strptime(line_spl[2], "%Y-%m-%d"), float(line_spl[3]),
            float(line_spl[4]),
            float(line_spl[5]), line_spl[6], url_find, tag_find)
        # print line_spl
        weibo_list.append(line_spl)
    file_in.close()
    return weibo_list


def read_predict_data(*par):
    temp = par[0] if len(par) > 0 else None
    file_in = open("weibo_predict_data.txt")
    weibo_precict_data = []
    for line in file_in.readlines()[:temp]:
        # print line
        line_spl = line.split()
        content = (' ').join(line_spl[3:])  # 提取内容
        url_find = URL_PATT.findall(content)
        tag_find = TAG_PATT.findall(content)
        line_spl = line_spl[0:3] + [content]
        # print line
        line_spl = (
            line_spl[0], line_spl[1], datetime.strptime(line_spl[2], "%Y-%m-%d"), line_spl[3], url_find, tag_find)
        weibo_precict_data.append(line_spl)
    file_in.close()
    return weibo_precict_data
