__author__ = 'key'
from constant import *
from datetime import *
from sta_inf import FCL
from sklearn.ensemble import RandomForestClassifier


def get_sta(now_date, url_find, day_url_count):
    count = FCL()
    count.init_zero()
    for url in url_find:
        for delta in range(STA_DAY):
            day = now_date - timedelta(days=delta)
            if day in day_url_count:
                url_count = day_url_count[day]
                if url in url_count:
                    count.forward += url_count[url].forward
                    count.comment += url_count[url].comment
                    count.like += url_count[url].like
    count.forward = (count.forward + 1) / len(url_find) if len(url_find) > 0 else 0
    count.comment = (count.comment + 1) / len(url_find) if len(url_find) > 0 else 0
    count.like = (count.like + 1) / len(url_find) if len(url_find) > 0 else 0
    return count


# 输出预测结果
def print_predict(predict_list, rf_list, day_url_count, day_tag_count, user_count):
    f_out = open('predict_answer.txt', 'w')
    for wb in predict_list:
        uid = wb[0]
        mid = wb[1]
        now_date = wb[2]
        url_find = wb[4]
        tag_find = wb[5]
        url_sta = get_sta(now_date, url_find, day_url_count)
        tag_sta = get_sta(now_date, tag_find, day_tag_count)
        url_fea = [url_sta.forward, url_sta.comment, url_sta.like]
        tag_fea = [tag_sta.forward, tag_sta.comment, tag_sta.like]
        if uid in user_count:
            avg_forward = user_count[uid].get_avg_forward()
            avg_comment = user_count[uid].get_avg_comment()
            avg_like = user_count[uid].get_avg_like()
            all_fea = url_fea + tag_fea + [avg_forward, avg_comment, avg_like]
            forward = rf_list[0].predict(all_fea)
            comment = rf_list[1].predict(all_fea)
            like = rf_list[2].predict(all_fea)
        else:
            part_fea = url_fea + tag_fea
            forward = rf_list[3].predict(part_fea)
            comment = rf_list[4].predict(part_fea)
            like = rf_list[5].predict(part_fea)
        print >> f_out, '%s\t%s\t%d,%d,%d' % (uid, mid, forward, comment, like)
    f_out.close()


# 提取特征
def get_train_feature(train_list, day_url_count, day_tag_count, user_count):
    all_feature = []
    part_feature = []
    for wb in train_list:
        uid = wb[0]
        date = wb[2]
        url_find = wb[7]
        tag_find = wb[8]
        url_sta = get_sta(date, url_find, day_url_count)  # 该微薄包含的url在STA_DAY天内的平均转发数
        tag_sta = get_sta(date, tag_find, day_tag_count)  # 含义同上
        avg_forward = user_count[uid].get_avg_forward()  # 该用户发表微薄的平均转发数
        avg_comment = user_count[uid].get_avg_comment()  # 同上
        avg_like = user_count[uid].get_avg_like()  # 同上
        url_fea = [url_sta.forward, url_sta.comment, url_sta.like]
        tag_fea = [tag_sta.forward, tag_sta.comment, tag_sta.like]
        all_feature.append(url_fea + tag_fea + [avg_forward, avg_comment, avg_like])  # 所有特征的列表，用于训练测试集中用户出现在训练及中的情况
        part_feature.append(url_fea + tag_fea)  # 部分特征的列表，用于训练测试集中用户没有出现在训练及中的情况
    return all_feature, part_feature


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
