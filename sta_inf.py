# coding:UTF-8
__author__ = 'key'


# 保存转发，评论，赞数
class FCL:
    def __init__(self, *par):
        self.weibo_num, self.forward, self.comment, self.like = par

    def get_avg_forward(self):  # 用户每条微薄的平均转发数
        return self.forward / self.weibo_num

    def get_avg_comment(self):
        return self.comment / self.weibo_num

    def get_avg_like(self):
        return self.like / self.weibo_num


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
            url_list[v] = FCL(0, 0, 0, 0)
    return url_list


# 获取微薄的统计信息，用于后面特征提取
def get_sta_inf(train_list):
    day_url_count = {}  # 按天记录url的统计信息(转发/评论/赞)，也就是某一天，某个url被所有微薄转发/评论/赞的次数
    day_tag_count = {}  # 按天记录tag的统计信息(转发/评论/赞)，含义同上
    user_day_name = {}  # 记录用户每天的微博数,转发/评论/赞的统计信息
    for wb in train_list:
        uid = wb[0]
        date = wb[2]
        forward = wb[3]
        comment = wb[4]
        like = wb[5]
        url_find = wb[7]
        tag_find = wb[8]
        day_url_count[date] = get_url_tag_list(date, url_find, forward, comment, like, day_url_count)
        day_tag_count[date] = get_url_tag_list(date, tag_find, forward, comment, like, day_tag_count)
        if uid in user_day_name:
            user_inf = user_day_name[uid]
            if date in user_inf:
                user_inf[date].weibo_num += 1.0
                user_inf[date].forward += forward
                user_inf[date].comment += comment
                user_inf[date].like += like
            else:
                user_inf[date] = FCL(1.0, forward, comment, like)
        else:
            user_day_name[uid] = {}

    return day_url_count, day_tag_count, user_day_name
