# coding:UTF-8
__author__ = 'key'
from  datetime import *
from constant import *
import re


def read_train_data(*par):
    temp = par[0] if len(par) > 0 else None
    file_in = open("data/weibo_train_data.txt")
    weibo_list = []
    for line in file_in.readlines()[:temp]:
        # print line
        line_spl = line.split()
        content = (' ').join(line_spl[6:])  # 提取内容
        url_find = URL_PATT.findall(content)  # 包含的url的列表；
        tag_find = TAG_PATT.findall(content)  # 包含的tag的列表；
        user_find = USER_PATT.findall(content)
        line_spl = line_spl[0:6] + [content]
        line_spl = (
            line_spl[0], line_spl[1], datetime.strptime(line_spl[2], "%Y-%m-%d"), float(line_spl[3]),
            float(line_spl[4]),
            float(line_spl[5]), line_spl[6], url_find, tag_find, user_find)
        # print line_spl
        weibo_list.append(line_spl)
    file_in.close()
    return weibo_list


def read_predict_data(*par):
    temp = par[0] if len(par) > 0 else None
    file_in = open("data/weibo_predict_data.txt")
    weibo_precict_data = []
    for line in file_in.readlines()[:temp]:
        # print line
        line_spl = line.split()
        content = (' ').join(line_spl[3:])  # 提取内容
        url_find = URL_PATT.findall(content)
        tag_find = TAG_PATT.findall(content)
        user_find = USER_PATT.findall(content)
        line_spl = line_spl[0:3] + [content]
        # print line
        line_spl = (
            line_spl[0], line_spl[1], datetime.strptime(line_spl[2], "%Y-%m-%d"), line_spl[3], url_find, tag_find,
            user_find)
        weibo_precict_data.append(line_spl)
    file_in.close()
    return weibo_precict_data


def read_train_feature():
    file_all = open('data/train_all_feature.txt')
    all_feature = []
    part_feature = []
    for ls in file_all.readlines():
        ls = re.sub(r'[\[\,\]]', ' ', ls)
        line_spl = map(eval, ls.split())
        all_feature.append(line_spl)

    file_all.close()
    file_part = open('data/train_part_feature.txt')
    for ls in file_part.readlines():
        ls = re.sub(r'[\[\,\]]', ' ', ls)
        line_spl = map(eval, ls.split())
        part_feature.append(line_spl)
    file_part.close()
    return all_feature, part_feature


def read_train_label():
    train_label = []
    file_label = open('data/train_label.txt')
    for ls in file_label.readlines():
        train_label.append(eval(ls))
    file_label.close()
    return train_label


def print_train_feature(all_feature, part_feature):
    file_all = open('data/train_all_feature.txt', 'w')
    for ls in all_feature:
        print>> file_all, ls
    file_all.close()
    file_part = open('data/train_part_feature.txt', 'w')
    for ls in part_feature:
        print>> file_part, ls
    file_part.close()


def print_train_label(label_list):
    file_label = open('data/train_label.txt', 'w')
    for ls in label_list:
        print>> file_label, ls
    file_label.close()
