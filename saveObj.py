__author__ = 'key'


# 将对象保存在文件中
def save_obj(obj, file_name):
    f1 = file(file_name, 'wb')
    pickle.dump(obj, f1, True)
    f1.close()


# 从文件中读取对象
def read_obj(file_name):
    f2 = file(file_name, 'rb')
    return pickle.load(f2)
