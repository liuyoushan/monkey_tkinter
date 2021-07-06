# -*- coding:utf-8 -*-
import re
import monkey


class read_file:
    def __init__(self):
        self.file_path = monkey.PATH_error

    def file(self):
        with open(self.file_path, 'r') as f:
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
            if 'CRASH' in s[i]:
                print('出现crash:{}'.format(s[i]))
                log_keyword = re.findall('Msg: (.*)', s[i + 1])
                page_name = re.findall('CRASH: (.*?) \(', s[i])
                res = 'CRASH', i + 1, log_keyword, page_name
                str1.append(res)

            elif 'ANR' in s[i]:
                print('出现ANR:{}'.format(s[i]))
                log_keyword = re.findall('Msg: (.*)', s[i + 1])
                page_name = re.findall('ANR: (.*?) \(', s[i])
                res = 'CRASH', i + 1, log_keyword, page_name
                str1.append(res)
        return str1


if __name__ == '__main__':
    read_file().get_file()
