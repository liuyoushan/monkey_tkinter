# -*- coding:utf-8 -*-
import re
import monkey

'''
log_analysis主要是日志分析相关
'''
ErrorKeywordList = ['CRASH', 'ANR']


# 封装匹配异常关键字方法
def re_keyword(s, i, keyword_1, keyword_2):
    try:
        log_keyword = re.findall('{}: (.*)'.format(keyword_2), s[i + 1])
        page_name = re.findall('{}: (.*?) \('.format(keyword_1), s[i])
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


class read_file:
    def __init__(self, path):
        self.path = path

    # 按行读取文件
    def file(self):
        with open(self.path, 'r') as f:
            n = 0
            str1 = []
            for i in f.readlines():
                logs = '{}行:'.format(n) + i
                n += 1
                str1.append(logs)
            return str1

    def get_file(self):
        s = self.file()
        str1 = []
        for i in range(29, len(s)):
            if 'CRASH' in s[i] or 'crash' in s[i]:
                # print('出现CRASH:{}'.format(s[i]))
                re_keyword_ = re_keyword(s, i, 'CRASH', 'Msg')
                res = 'CRASH', i + 1, re_keyword_[0], re_keyword_[1]
                print(res)
                str1.append(res)

            elif 'ANR' in s[i] or 'anr' in s[i]:
                re_keyword_ = re_keyword(s, i, 'ANR', 'Msg')
                res = 'ANR', i + 1, re_keyword_[0], re_keyword_[1]
                print(res)
                str1.append(res)
        # print(str1)
        return str1


if __name__ == '__main__':
    read_file().get_file()
