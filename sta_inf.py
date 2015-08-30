# coding:UTF-8
__author__ = 'key'


# 保存转发，评论，赞数
class FCL:
    def __init__(self):
        self.uid_count = 1.0  # 计算该用户出现了多少次，也就是发表了多少微薄
        self.forward = 1.0
        self.comment = 1.0
        self.like = 1.0

    def init_zero(self):
        self.uid_count = 0.0
        self.forward = 0.0
        self.comment = 0.0
        self.like = 0.0

    def get_avg_forward(self):  # 用户每条微薄的平均转发数
        return self.forward / self.uid_count

    def get_avg_comment(self):
        return self.comment / self.uid_count

    def get_avg_like(self):
        return self.like / self.uid_count


# 用于get_sta_inf函数
def get_url_tag_list(date, url_find, forward, comment, like, day_url_count):
    if date in day_url_count:
        url_list = day_url_count[date]
    else:
        url_list = {}
    for v in url_find:
        if v in url_list:
            url_list[v].forward += forward
            url_list[v].comment += comment
            url_list[v].like += like
        else:
            url_list[v] = FCL()
    return url_list


# 获取微薄的统计信息，用于后面特征提取
def get_sta_inf(train_list):
    day_url_count = {}  # 按天记录url的统计信息(转发/评论/赞)，也就是某一天，某个url被所有微薄转发/评论/赞的次数
    day_tag_count = {}  # 按天记录tag的统计信息(转发/评论/赞)，含义同上
    user_count = {}  # 记录用户历史微博数,转发/评论/赞的统计信息
    for wb in train_list:
        uid = wb[0]
        date = wb[2]
        forward = wb[3] + 1.0
        comment = wb[4] + 1.0
        like = wb[5] + 1.0
        url_find = wb[7]
        tag_find = wb[8]
        day_url_count[date] = get_url_tag_list(date, url_find, forward, comment, like, day_url_count)
        day_tag_count[date] = get_url_tag_list(date, tag_find, forward, comment, like, day_tag_count)
        if uid in user_count:
            user_count[uid].uid_count += 1.0
            user_count[uid].forward += forward
            user_count[uid].comment += comment
            user_count[uid].like += like
        else:
            user_count[uid] = FCL()
            user_count[uid].forward = forward
            user_count[uid].comment = comment
            user_count[uid].like = like
            #     uid_like[uid] = like
    return day_url_count, day_tag_count, user_count
