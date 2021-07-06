# -*- coding: utf-8 -*-
import time, os, re, sys

rune_state = False
# 日志写入路径
PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
PATH_info = os.path.join(PATH, 'info.txt')
PATH_error = os.path.join(PATH, 'error.txt')


# 查找手机设备
def devices():
    device = os.popen('adb devices').read()
    if device:
        r = re.findall(r'attached\n(.*?)\tdevice', device)
        r = [i for i in r if r != '']
        return r
    else:
        return False


def runmonkey(parameter):
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
                pp3=parameter['run_bfb3'], PATH_info=PATH_info, PATH_error=PATH_error, crash=crash_if)
    print('info：运行命令:{}\n'.format(monkeycmd))

    # 查找安装包
    cad = 'adb -s {device} shell pm list package "|grep {page}"'.format(device=device, page=parameter['page'])
    pagename = os.popen(cad).read()

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
    if device:
        page_name = 'adb -s {device} shell dumpsys window w | findstr \/ | findstr name='.format(device=device[0])
        w = os.popen(page_name).read()
        ws = re.findall('mSurface=Surface\(name=(.*?)/com', w)
        if ws:
            return ws[0]
        else:
            raise NameError('未获取到包名')
