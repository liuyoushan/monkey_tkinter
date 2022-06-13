# -*- coding: utf-8 -*-
import time, os, re, sys, datetime

rune_state = False

PATH = os.path.dirname(os.path.realpath(sys.argv[0]))


def log_path():
    '''
    每次运行请求此方法时，文件名：获取当前时间+文件名
    :return:
    '''
    now = datetime.datetime.now().strftime("%Y-%m-%d~%H'%M'%S")
    # 日志写入路径
    PATH_info = os.path.join(PATH, str(now) + '_INFO.txt')
    PATH_error = os.path.join(PATH, str(now) + '_ERROR.txt')
    return PATH_info, PATH_error, PATH


# 获取最新的error文件
def newest():
    files = os.listdir(PATH)
    # paths = [os.path.join(path, basename) for basename in files]
    paths = [os.path.join(PATH, basename) for basename in files if 'ERROR' in basename]
    return max(paths, key=os.path.getctime)


# 获取目录下所有txt文件
def get_file_txt():
    # path = sys.argv[0]  # 获取本文件路径
    # filename = os.path.basename(path)  # 获取本文件名
    # path = os.path.dirname(os.path.realpath(sys.argv[0]))  # 获取本文件所在目录
    # filelist = os.listdir(path)  # 获取文件名列表
    # filelist.remove(filename)  # 从目录的文件里面去除本文件的文件名
    try:
        filelist = os.listdir(PATH)
        a = []
        for i in filelist:
            if '.txt' in i:
                a.append(i)
        if not a:
            a.append('无txt文件')
        return a
    except NameError as e:
        print(e)


# 查找手机设备
def devices():
    device = os.popen('adb devices').read()
    if device:
        r = re.findall(r'attached\n(.*?)\tdevice', device)
        r = [i for i in r if r != '']
        return r
    else:
        return False


def runmonkey(parameter, get_nowTime):
    '''

    :param parameter: 需要运行的命令参数
    :return:
    '''

    global rune_state
    if devices():
        device = devices()[0]
    else:
        raise NameError('手机设备未找到，请查看手机设备连接是否正常')

    # 判断'--ignore-crashes'是否开启
    crash_if = '--ignore-crashes' if parameter['crash_is'] == '开启' else ''

    monkeycmd = "adb -s {device} shell monkey -p {page} " \
                "--ignore-timeouts {crash} --kill-process-after-error " \
                "{p1} {pp1} {p2} {pp2} {p3} {pp3}  " \
                "--throttle {ms} -v -v -v {click} 2>{PATH_error} 1>{PATH_info}" \
        .format(device=device, page=parameter['page'], ms=parameter['ms'],
                click=parameter['click'], p1=parameter['run_p1'], p2=parameter['run_p2'],
                p3=parameter['run_p3'], pp1=parameter['run_bfb1'], pp2=parameter['run_bfb2'],
                pp3=parameter['run_bfb3'], PATH_info=get_nowTime[0], PATH_error=get_nowTime[1], crash=crash_if)
    print('info：运行命令:{}\n'.format(monkeycmd))

    # 查找安装包
    cad = 'adb -s {device} shell pm list package "|grep {page}"'.format(device=device, page=parameter['page'])
    pagename = os.popen(cad).read()
    # 判断是否安装了用户输入的包名，没有则提示用户安装
    if pagename:
        rune_state = True
        os.popen(monkeycmd)
        print('info：start running monkey')

        time.sleep(2)
        while True:
            time.sleep(1)
            ps = psGrepMonkey()  # 监控进程
            # print(ps)
            if ps is False:
                rune_state = False
                break
    else:
        raise NameError('ERROR: {}包名未找到，请确认包是否正常安装，或设备连接是否正常'.format(parameter['page']))


# 查找monkey进程
def psGrepMonkey():
    if devices():
        ps_pid = os.popen('adb -s {} shell ps | findstr  monkey'.format(devices()[0])).read()
        if ps_pid:
            s = ps_pid.split(' ')
            s = [i for i in s if i != '']
            # print(s)
            return s[1]
        else:
            return False
    else:
        raise NameError('手机设备未找到')


# 结束monkey进程
def end_monkey():
    monkey_thread = psGrepMonkey()
    if monkey_thread:
        kill_monkey = 'adb -s {device} shell kill {ps}'.format(device=devices()[0], ps=monkey_thread)
        os.popen(kill_monkey)
        print('info：结束monkey进程：{}'.format(monkey_thread))
        return True
    else:
        print('结束进程操作失败，未找到monkey进程')
        return False


# 获取运行中的包名类名
def get_page():
    device = devices()
    print(device,type(device))
    if device:
        page_name = 'adb -s {device} shell dumpsys window w | findstr \/ | findstr name='.format(device=device[0])
        w = os.popen(page_name).read()
        print(w)
        ws = re.findall('mSurface=Surface\(name=(.*?)/(.*?)\)', w)
        print(ws)
        if ws:
            return ws[0][0]
        else:
            return False
    else:
        return False

