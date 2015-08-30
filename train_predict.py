# coding:UTF-8
__author__ = 'key'
from sklearn.ensemble import RandomForestClassifier
from feature import get_sta, compute_avg_FCL
from constant import *


# 暂时没用到
def get_label(forward):
    weibo_class = []
    max_forward = max(forward)
    for v in forward:
        if v > max_forward * 0.96:
            weibo_class.append(1)
        elif v > max_forward * 0.8:
            weibo_class.append(2)
        else:
            weibo_class.append(3)
    return weibo_class


# 输出预测结果
def print_predict(predict_list, rf_list, day_url_count, day_tag_count, user_day_count):
    f_out = open('data/predict_answer.txt', 'w')
    for wb in predict_list:
        uid = wb[0]
        mid = wb[1]
        now_date = wb[2]
        url_find = wb[4]
        tag_find = wb[5]
        user_find = wb[6]
        url_sta = get_sta(now_date, url_find, day_url_count)
        tag_sta = get_sta(now_date, tag_find, day_tag_count)
        url_fea = [len(url_find), url_sta.forward, url_sta.comment, url_sta.like]
        tag_fea = [len(tag_find), tag_sta.forward, tag_sta.comment, tag_sta.like]
        if uid in user_day_count:
            avg_forward, avg_comment, avg_like = compute_avg_FCL(user_day_count, uid, now_date)
            all_fea = url_fea + tag_fea + [len(user_find)] + [avg_forward, avg_comment, avg_like]
            forward = rf_list[0].predict(all_fea)
            comment = rf_list[1].predict(all_fea)
            like = rf_list[2].predict(all_fea)
        else:
            part_fea = url_fea + tag_fea + [len(user_find)]
            forward = rf_list[3].predict(part_fea)
            comment = rf_list[4].predict(part_fea)
            like = rf_list[5].predict(part_fea)
        print >> f_out, '%s\t%s\t%d,%d,%d' % (uid, mid, forward, comment, like)
    f_out.close()


# 用随机森林训练
def train(all_feature, part_feature, train_list):
    rf_list = []
    forward_label = zip(*train_list)[3]
    comment_label = zip(*train_list)[4]
    like_label = zip(*train_list)[5]
    for i in range(6):
        rf_list.append(RandomForestClassifier(random_state=0, n_estimators=RF_NUMBER, max_depth=MAX_DEPTH))
    rf_list[0].fit(all_feature, forward_label)  # forward_label
    rf_list[1].fit(all_feature, comment_label)  # comment_label
    rf_list[2].fit(all_feature, like_label)  # like_label
    rf_list[3].fit(part_feature, forward_label)
    rf_list[4].fit(part_feature, comment_label)
    rf_list[5].fit(part_feature, like_label)
    return rf_list
    # kf = cross_validation.KFold(len(weibo_forward), n_folds=10)
    # scores = cross_val_score(clf, weibo_vector,weibo_forward,cv=kf)
    # print scores.mean()
