# coding:UTF-8
__author__ = 'key'
from constant import *
from datetime import *
from sta_inf import FCL


def get_sta(now_date, url_find, day_url_count):
    count = FCL(0, 0, 0, 0)
    for url in url_find:
        for delta in range(STA_DAY):
            day = now_date - timedelta(days=delta + 1)
            if day in day_url_count:
                url_count = day_url_count[day]
                if url in url_count:
                    count.forward += url_count[url].forward
                    count.comment += url_count[url].comment
                    count.like += url_count[url].like
    count.forward = count.forward / len(url_find) if len(url_find) > 0 else 0
    count.comment = count.comment / len(url_find) if len(url_find) > 0 else 0
    count.like = count.like / len(url_find) if len(url_find) > 0 else 0
    return count


def compute_avg_FCL(user_day_count, uid, now_date):
    weibo_num = 0
    forward = 0
    comment = 0
    like = 0
    for delta in range(STA_DAY):
        day = now_date - timedelta(days=delta + 1)
        if day in user_day_count[uid]:
            weibo_num += user_day_count[uid][day].weibo_num
            forward += user_day_count[uid][day].forward
            comment += user_day_count[uid][day].comment
            like += user_day_count[uid][day].like
    avg_forward = forward / weibo_num if weibo_num > 0 else 0
    avg_comment = comment / weibo_num if weibo_num > 0 else 0
    avg_like = like / weibo_num if weibo_num > 0 else 0
    return avg_forward, avg_comment, avg_like


# 提取特征
def get_train_feature(train_list, day_url_count, day_tag_count, user_day_count):
    all_feature = []
    part_feature = []
    for wb in train_list:
        uid = wb[0]
        now_date = wb[2]
        url_find = wb[7]
        tag_find = wb[8]
        user_find = wb[9]
        url_sta = get_sta(now_date, url_find, day_url_count)  # 该微薄包含的url在STA_DAY天内的平均转发数
        tag_sta = get_sta(now_date, tag_find, day_tag_count)  # 含义同上
        avg_forward, avg_comment, avg_like = compute_avg_FCL(user_day_count, uid, now_date)  # 计算用户STA——DAY内的每条微博的FCL均数
        url_fea = [len(url_find), url_sta.forward, url_sta.comment, url_sta.like]
        tag_fea = [len(tag_find), tag_sta.forward, tag_sta.comment, tag_sta.like]
        all_feature.append(
            url_fea + tag_fea + [len(user_find)] + [avg_forward, avg_comment, avg_like])  # 所有特征的列表，用于训练测试集中用户出现在训练及中的情况
        part_feature.append(url_fea + tag_fea + [len(user_find)])  # 部分特征的列表，用于训练测试集中用户没有出现在训练及中的情况
    return all_feature, part_feature
