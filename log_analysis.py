# -*- coding:utf-8 -*-
import re
import os

'''
log_analysis主要是日志分析相关
'''
# 异常关键字配置
ErrorKeywordList = ('CRASH', 'ANR', 'crash', 'anr')


# 封装异常关键字匹配的正则方法
def re_keyword(data, line_number, keyword_1, keyword_2):
    """
    :param data: log数据
    :param line_number: log行数
    :param keyword_1:   异常关键字，用来匹配包名
    :param keyword_2:   关键字，用来匹配异常数据的第二行。匹配表格列表的“异常关键字”
    :return:    包名，异常关键字
    """
    try:
        log_keyword = re.findall('{}: (.*)'.format(keyword_2), data[line_number + 1])
        page_name = re.findall('{}: (.*?) \('.format(keyword_1), data[line_number])
    except:
        # 匹配失败则默认给个斜杠
        log_keyword = '\\'
        page_name = '\\'

    # 匹配的（列表）结果为空，则默认斜杠
    if not log_keyword:
        log_keyword = '\\'
    elif not page_name:
        page_name = '\\'

    return page_name, log_keyword


class ReadFile:
    def __init__(self, path):
        self.path = path

    # 按行读取文件
    def file(self):
        file_path = os.path.join(os.path.dirname(__file__), self.path)
        with open(file_path, 'r') as f:
            n = 0
            str1 = []
            for i in f.readlines():
                logs = '{}行:'.format(n) + i
                n += 1
                str1.append(logs)
            return str1

    # 判断是否存在指定关键字
    def get_file(self):
        # 按行读取的数据
        file_data = self.file()
        str1 = []
        # 从第29行开始遍历读取的数据
        for i in range(29, len(file_data)):
            # 遍历异常字段的配置
            for err_str in ErrorKeywordList:
                # 判断ErrorKeywordList的异常字段，如果存在于读取的那行数据里面，则进行匹配
                if err_str in file_data[i]:
                    # 正则匹配异常数据
                    page_name, log_keyword = re_keyword(file_data, i, err_str, 'Msg')
                    # 拼接报错信息
                    res = err_str, i + 1, page_name, log_keyword
                    # print(res)
                    str1.append(res)

        return str1


if __name__ == '__main__':
    ReadFile(0).get_file()
