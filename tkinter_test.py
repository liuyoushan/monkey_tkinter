# -*- coding: utf-8 -*-
import pyperclip
import log_analysis
import monkey
import threading
import datetime
import time, os
import tkinter  # 主窗口生成
import tkinter.messagebox  # 弹出对话框
from tkinter import *  # 运行按钮Button用到这个库
from tkinter import ttk  # 下拉框控件要用ttk
from tkinter import filedialog

from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'img.png')

# import matplotlib
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
tkinter_test类（页面控件显示相关的类，主运行层）
monkey主要是运行具体monkey命令，需要传入用户输入的运行命令参数
log_analysis主要是日志分析相关
打包方法：pyinstaller ***.py --add-data ".\*.png;."
'''

# 运行参数
run_test = ('--pct-touch', '--pct-motion', '--pct-trackball', '--pct-nav',
            '--pct-majornav', '--pct-syskeys', '--pct-appswitch', '--pct-anyevent', '--pct -anyevent',)
# 运行参数百分比
rg = [str(i) + '%' for i in range(1, 101)]
crash_is = ['开启', '关闭']


class MainPage:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.config(background='Gainsboro')
        self.not_empty = False


    def mainpage(self):
        root = self.root
        root.title('Monkey测试工具')
        root.geometry('1000x600')
        # 窗口大小设置，设置为false为不可调整大小
        root.resizable = False

        def img():
            global photo
            # 增加背景图片,如果在方法里面使用，需要先将photo声明全局变量
            photo = tkinter.PhotoImage(file=path_to_dat)
            theLabel = tkinter.Label(root,
                                     # 内容
                                     justify=tkinter.LEFT,
                                     # 对齐方式
                                     image=photo,
                                     # 加入图片
                                     compound=tkinter.CENTER,
                                     # 关键:设置为背景图片
                                     font=("华文行楷", 20),
                                     # 字体和字号
                                     fg="white")  # 前景色
            theLabel.pack()

        img()

        # ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇按钮控件⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇
        Label(root, text='包名:').place(x=10, y=10)
        # 给输入框默认值
        addr = tkinter.StringVar()
        addr.set('点击获取→')
        # 包名输入框控件
        self.page = Entry(root, bd=5, bg='white', textvariable=addr)
        self.page.place(x=90, y=10)
        Label(root, text='Click总数:').place(x=10, y=45)
        # click输入框
        self.click = Entry(root, bd=5, bg='white')
        self.click.place(x=90, y=45)

        Label(root, text='间隔时间ms:').place(x=10, y=80)
        self.ms = Entry(root, bd=5, bg='white')
        self.ms.place(x=90, y=80)
        # 是否忽略崩溃
        Label(root, text='忽略崩溃:').place(x=10, y=125)
        # 下拉框，设置默认值为第一个字符串
        self.crash_is = ttk.Combobox(root, value=crash_is, state='readonly')
        self.crash_is.place(x=90, y=125)
        self.crash_is.current(0)

        '''
        需求:实现点击添加按钮新增运行参数控件
        修改:想重构.把运行参数控件的,所有下拉控件添加到一个列表,实现上述需求
        '''
        self.num = 0  # 参数名称自增
        self.optionmenu_y = 45  # 起始位置
        self.run_optionmenu_list = []
        self.percentage_optionmenu_list = []
        self.label_title = []

        def add_OptionMenu():
            self.optionmenv_num = 'opName'
            if self.num < 6:
                # 控件名称数字&y轴位置
                self.num += 1
                self.optionmenu_y += 60

                # 运行参数label
                opt_1 = Label(root, text='运行参数{}：'.format(self.num))
                # 运行参数下拉框
                opt_2 = ttk.Combobox(root, value=run_test, state='readonly')
                opt_2.current(0)
                # 运行参数百分比
                opt_3 = ttk.Combobox(root, value=rg, state='readonly')
                opt_3.current(9)

                # 控件添加到数组
                self.label_title.append(opt_1)
                self.run_optionmenu_list.append(opt_2)
                self.percentage_optionmenu_list.append(opt_3)
                # 显示到页面
                opt_1.place(x=10, y=self.optionmenu_y + 60)
                opt_2.place(x=90, y=self.optionmenu_y + 60)
                opt_3.place(x=90, y=self.optionmenu_y + 85)
            else:
                print('最多添加6个')

        add_OptionMenu()    # 默认显示一个
        Button(root, text='+', takefocus=0, command=add_OptionMenu, bg='Gainsboro', width=2, height=0,
               font=('Helvetica', '10')).place(x=255, y=165)

        # 删除运行参数下拉控件
        def delete_optionmenu():
            if len(self.label_title) > 1:
                # 控件名称数字&y轴位置
                self.num -= 1
                self.optionmenu_y -= 60
                # 删除控件
                self.run_optionmenu_list[-1].destroy()
                self.percentage_optionmenu_list[-1].destroy()
                self.label_title[-1].destroy()
                # 清除列表最后一个控件
                del self.run_optionmenu_list[-1]
                del self.percentage_optionmenu_list[-1]
                del self.label_title[-1]
            else:
                print('最后一个不能删除')
        Button(root, text='-', takefocus=0, command=delete_optionmenu, bg='Gainsboro', width=2, height=0,
               font=('Helvetica', '10')).place(x=280, y=165)

        Label(self.root, text='开始时间:').place(x=850, y=500)
        Label(self.root, text='结束时间:').place(x=850, y=520)
        Label(self.root, text='计时(s):').place(x=850, y=540)

        # 可点击按钮控件，需要用到包from tkinter import *
        Button(root, text='运行', takefocus=0, command=self.run_thread, bg='green', width=8, height=0,
               font=('Helvetica', '10')).place(x=10, y=550)
        Button(root, text='结束运行', takefocus=0, command=self.end_run, bg='red', width=8, height=0,
               font=('Helvetica', '10')).place(x=90, y=550)
        Button(root, text='分析文件日志', takefocus=0, command=self.inster_data, bg='Gainsboro', width=10, height=0,
               font=('Helvetica', '10')).place(x=680, y=10)
        Button(root, text='清空表格', takefocus=0, command=self.clear_data, bg='Gainsboro', width=8, height=0,
               font=('Helvetica', '10')).place(x=720, y=280)

        # 自动获取包名
        def btnClick():
            s = monkey.get_page()
            if s:
                # 复制到剪切板
                pyperclip.copy(s)
                tkinter.messagebox.showinfo("提示", '已复制到剪切板！\n包名：{}'.format(s))
            else:
                tkinter.messagebox.showinfo("提示", '复制失败！\n未获取到包名，请检查设备连接是否正常')

        Button(root, text='获取', takefocus=0, command=btnClick, width=3, height=0, bg='Gainsboro',
               font=('Helvetica', '10')).place(x=245, y=10)

        def file_path():
            # lists = monkey.get_file_txt()
            Label(root, text='选择文件：').place(x=310, y=10)
            # 下拉框，设置默认值为第一个字符串
            self.file_list = ttk.Combobox(root, value=monkey.get_file_txt(), width=27, state='readonly')
            self.file_list.place(x=385, y=10)
            self.file_list.current(0)

        file_path()
        Button(root, text='更新文件', takefocus=0, command=file_path, bg='Gainsboro', width=6, height=0,
               font=('Helvetica', '10')).place(x=610, y=10)
        # 创建表格控件
        self.tree_date = ttk.Treeview(root, show='headings')
        tree_date = self.tree_date

        # 竖直滚动条
        ybar = ttk.Scrollbar(root, orient='vertical')
        ybar.place()
        ybar.config(command=self.tree_date.yview)
        tree_date.configure(yscrollcommand=ybar.set)

        # 创建表格显示日志异常信息
        def table():
            # 创建表格
            tree_date['columns'] = ['类型', '行数', '包名', '异常关键字']
            tree_date.place(x=310, y=40)

            # 设置列宽度
            tree_date.column('异常关键字', width=300)
            tree_date.column('包名', width=100)
            tree_date.column('行数', width=50, anchor=S)
            tree_date.column('类型', width=50, anchor=S)

            # 添加列名
            tree_date.heading('类型', text='类型')
            tree_date.heading('异常关键字', text='异常关键字')
            tree_date.heading('包名', text='包名')
            tree_date.heading('行数', text='行数')

            tree_date.insert('', 1, text='', values=('', '', '', '运行完成后可点击查看异常日志'))

        table()
        # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
        root.mainloop()

    # 确认框
    def end_run(self):
        a = tkinter.messagebox.askokcancel('提示', '要执行此操作吗？')
        if a:
            monkey.end_monkey()

    def run_thread(self):
        self.threads = []
        t = threading.Thread(target=self.init_str, args=())
        self.threads.append(t)
        ts = threading.Thread(target=self.runtime, args=())
        self.threads.append(ts)
        for i in self.threads:
            i.start()

    def init_str(self):
        dicts = {}
        # 调用方法，run_data_list的所有参数数据处理，匹配并且添加到列表
        run_data_list = []
        for r, p in zip(self.run_optionmenu_list, self.percentage_optionmenu_list):
            run_data_list.append([r.get(), re.sub('\D', '', p.get())])
        dicts['page'] = self.page.get()
        dicts['click'] = self.click.get()
        dicts['ms'] = self.ms.get()
        dicts['crash_is'] = self.crash_is.get()
        dicts['run_data_list'] = run_data_list
        # self.not_empty = False
        for k, v in dicts.items():
            if k not in ['run_data_list', 'crash_is']:  # 判断字典key，如果是列表不包含的字符继续执行（因为数据不一样，包含字符串和列表。下面的判断会出问题）
                if v.strip() == '':  # 如果为空，那么修改指标变量为False.并且弹出提示不能为空。并且退出所有循环。
                    tkinter.messagebox.showinfo("提示", '{}不能为空'.format(k))
                    self.not_empty = False
                    break
            else:
                continue
            # 如果能顺利循环完成，那改为True
            self.not_empty = True

        if self.not_empty:
            monkey.runmonkey(dicts, monkey.log_path())

    # 运行计时
    def runtime(self):
        Label(self.root, text=datetime.datetime.now().strftime('%H:%M:%S')).place(x=920, y=500)
        while True:
            starttime = time.time()
            print('----------------------------------------------------------')
            print('开始计时')
            while True:
                times = round(time.time() - starttime, 0)
                time.sleep(1)
                Label(self.root, text=times).place(x=920, y=540)
                if monkey.rune_state is False:
                    print('退出计时')
                    Label(self.root, text=datetime.datetime.now().strftime('%H:%M:%S')).place(x=920, y=520)
                    break
            break

    def inster_data(self):
        self.clear_data()
        logs = log_analysis.read_file(self.file_list.get()).get_file()
        if logs:
            for i in range(len(logs)):
                # 给表格中添加数据
                self.tree_date.insert('', END, text='', values=(logs[i][0], logs[i][1], logs[i][2], logs[i][3]))
        else:
            print('未收集到异常日志')
            self.tree_date.insert('', 1, text='未收集到异常日志', values=('', '', '', '未收集到异常日志'))

    def clear_data(self):
        x = self.tree_date.get_children()
        for item in x:
            self.tree_date.delete(item)

    # # 创建柱状图
    # def plt(self):
    #     '''
    #     如果要将matplotlib生成图表和Tkinter生成的GUI程序关联起来，需要以下3个步骤：
    #     1、创建Matplotlib的figure(画布)对象，并在figure上进行绘图。
    #     2、创建FigureCanvasTkAgg(画布容器)对象，参数为第1步生成的figure对象和容器存放的父对象，并调用创建对象的draw函数。
    #     3、调用FigureCanvasTkAgg对应组件的Pack方法，将对象显示在页面上。
    #     :return:
    #     '''
    #     PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    #     PATH = os.path.join(PATH, 'SourceHanSansSC-Bold.otf')
    #     # fname 为 你下载的字体库路径，注意 SourceHanSansSC-Bold.otf 字体的路径(显示中文)
    #     zhfont1 = matplotlib.font_manager.FontProperties(fname=PATH)
    #
    #     x = [5, 2]
    #     v = ['CRASH','ANR']
    #     # 创建个空白图表
    #     fig = Figure(figsize=(3, 3))
    #     # 新增子图
    #     a = fig.add_subplot(111)
    #     # 创建柱状图
    #     a.bar(v, x, align='center')
    #     # a.invert_yaxis()  # 反转
    #     a.set_title("缺陷分布", fontsize=16, fontproperties=zhfont1)
    #
    #     canvas = FigureCanvasTkAgg(fig, master=self.root)
    #     canvas.get_tk_widget().place(x=300, y=280)
    #     canvas.draw()
    #     self.biaoge()


if __name__ == '__main__':
    p = MainPage().mainpage()
