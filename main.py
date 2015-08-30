# coding:UTF-8
import operator
from read_print import *
from sta_inf import *
from feature import get_train_feature
from train_predict import train, print_predict

train_list = read_train_data(100)  # 在read_data.py中
predict_list = read_predict_data(100)  # 在read_data.py中

day_url_count, day_tag_count, user_day_count = get_sta_inf(train_list)  # 在sta_inf.py中
all_feature, part_feature = get_train_feature(train_list, day_url_count, day_tag_count,
                                              user_day_count)  # 得到微薄的特征,在feature.py中

print_train_feature(all_feature, part_feature)  # 讲特征输出到文件
print_train_label(zip(*train_list)[3])  # 输出label到文件
label_list = read_train_label()  # 从文件读取label
all_feature, part_feature = read_train_feature()  # 从文件读取训练用的特征

rf_list = train(all_feature, part_feature, train_list)  # 在feature.py中，保存随机森林回归器
print_predict(predict_list, rf_list, day_url_count, day_tag_count, user_day_count)  # 在feature.py中






def print_weibo(weibo_list):
    for i in weibo_list:
        print i[0:6], i[6], i[7:]
