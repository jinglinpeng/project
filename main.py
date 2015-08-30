# coding:UTF-8
import time
import operator
import re
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
import cPickle as pickle
from read_data import *
from sta_inf import *
from feature import *

train_list = read_train_data()  # 在read_data.py中
predict_list = read_predict_data()  # 在read_data.py中

train_list = sorted(train_list, key=operator.itemgetter(3, 4, 5), reverse=True)[:500000]  # 按照转发数等排序,由于效率原因，只取一部分作为训练
# print train_list
day_url_count, day_tag_count, user_count = get_sta_inf(train_list)  # 在sta_inf.py中
all_feature, part_feature = get_train_feature(train_list, day_url_count, day_tag_count,
                                              user_count)  # 得到微薄的特征,在feature.py中

# all_feature=read_obj('all_feature')
# part_feature=read_obj('part_feature')
# day_url_count=read_obj('day_url_count')
# day_tag_count=read_obj('day_tag_count')
# user_count=read_obj('user_count')


rf_list = train(all_feature, part_feature, train_list)  # 在feature.py中，保存随机森林回归器
# save_obj(rf_list,'rf_list')
print_predict(predict_list, rf_list, day_url_count, day_tag_count, user_count)  # 在feature.py中


# day_url_count, day_tag_count, user_count=get_sta_inf(train_list)
# all_feature, part_feature=get_train_feature(train_list, day_url_count, day_tag_count, user_count)


# save_obj(day_url_count,'day_url_count')
# save_obj(day_tag_count,'day_tag_count')
# save_obj(user_count,'user_count')
# save_obj(all_feature,'all_feature')
# save_obj(part_feature,'part_feature')

# rf_list=train(all_feature,part_feature,train_list)
# save_obj(rf_list,'rf_list')
# print_predict(predict_list, rf_list, day_url_count, day_tag_count, user_count)


def print_weibo(weibo_list):
    for i in weibo_list:
        print i[0:6], i[6], i[7:]
