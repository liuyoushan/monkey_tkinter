# -*- coding: utf-8 -*-
import pyperclip
import log_analysis
import monkey
import threading
import datetime
import time
import tkinter  # 主窗口生成
import tkinter.messagebox  # 弹出对话框
from tkinter import *  # 运行按钮Button用到这个库
from tkinter import ttk  # 下拉框控件要用ttk


from os import path
import sys
bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'img.png')

# import matplotlib
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        Label(root, text='包名：').place(x=10, y=10)
        # 给输入框默认值
        addr = tkinter.StringVar()
        addr.set('点击获取→')
        self.page = Entry(root, bd=5, bg='white', textvariable=addr)
        self.page.place(x=90, y=10)
        Label(root, text='CLICK总数：').place(x=10, y=40)
        self.click = Entry(root, bd=5, bg='white')
        self.click.place(x=90, y=40)
        Label(root, text='间隔时间MS：').place(x=10, y=70)
        self.ms = Entry(root, bd=5, bg='white')
        self.ms.place(x=90, y=70)

        Label(root, text='运行参数1：').place(x=10, y=130)
        # 运行参数下拉框，设置默认值为第一个字符串
        self.run_p1 = ttk.Combobox(root, value=run_test)
        self.run_p1.place(x=90, y=130)
        self.run_p1.current(0)
        # 运行参数百分比
        self.run_bfb1 = ttk.Combobox(root, value=rg)
        self.run_bfb1.place(x=90, y=155)
        self.run_bfb1.current(9)

        Label(root, text='运行参数2：').place(x=10, y=190)
        # 下拉框，设置默认值为第一个字符串
        self.run_p2 = ttk.Combobox(root, value=run_test)
        self.run_p2.place(x=90, y=190)
        self.run_p2.current(0)
        self.run_bfb2 = ttk.Combobox(root, value=rg)
        self.run_bfb2.place(x=90, y=215)
        self.run_bfb2.current(9)

        Label(root, text='运行参数3：').place(x=10, y=250)
        # 下拉框，设置默认值为第一个字符串
        self.run_p3 = ttk.Combobox(root, value=run_test)
        self.run_p3.place(x=90, y=250)
        self.run_p3.current(0)
        self.run_bfb3 = ttk.Combobox(root, value=rg)
        self.run_bfb3.place(x=90, y=275)
        self.run_bfb3.current(9)

        # 是否忽略崩溃
        Label(root, text='忽略崩溃：').place(x=10, y=310)
        # 下拉框，设置默认值为第一个字符串
        self.crash_is = ttk.Combobox(root, value=crash_is)
        self.crash_is.place(x=90, y=310)
        self.crash_is.current(0)

        Label(self.root, text='开始时间：').place(x=10, y=450)
        Label(self.root, text='结束时间：').place(x=10, y=470)
        Label(self.root, text='运行计时(s)：').place(x=10, y=490)

        # 可点击按钮控件，需要用到包from tkinter import *
        Button(root, text='运行', takefocus=0, command=self.run_thread, bg='green', width=8, height=0,
               font=('Helvetica', '10')).place(x=10, y=380)
        Button(root, text='结束运行', takefocus=0, command=self.end_run, bg='red', width=8, height=0,
               font=('Helvetica', '10')).place(x=90, y=380)
        Button(root, text='异常日志', takefocus=0, command=self.inster_data, bg='Gainsboro', width=8, height=0,
               font=('Helvetica', '10')).place(x=310, y=10)
        Button(root, text='清空', takefocus=0, command=self.clear_data, bg='Gainsboro', width=8, height=0,
               font=('Helvetica', '10')).place(x=385, y=10)

        # 自动获取包名
        def btnClick():
            s = monkey.get_page()
            print(s)
            if s:
                # 复制到剪切板
                pyperclip.copy(s)
                tkinter.messagebox.showinfo("提示", '已复制到剪切板！\n包名：{}'.format(s))
            else:
                tkinter.messagebox.showinfo("提示", '复制失败！\n未获取到包名，请注意设备连接是否正常，包是否正常安装')

        Button(root, text='获取', takefocus=0, command=btnClick, width=3, height=0, bg='Gainsboro',
               font=('Helvetica', '10')).place(x=245, y=10)

        # 创建表格控件
        self.tree_date = ttk.Treeview(self.root)
        tree_date=self.tree_date
        # 创建表格显示日志异常信息
        def biaoge():
            # 创建表格
            tree_date['columns'] = ['类型', '行数', '错误日志']
            tree_date.place(x=310, y=40)
            # 设置列宽度
            tree_date.column('错误日志', width=300)
            tree_date.column('行数', width=50)
            tree_date.column('类型', width=50)
            # 添加列名
            tree_date.heading('错误日志', text='错误日志')
            tree_date.heading('行数', text='行数')
            tree_date.heading('类型', text='类型')
            tree_date.insert('', 1, text='运行完成后可点击查看异常日志', values=())

        biaoge()

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
        dicts['page'] = self.page.get()
        dicts['click'] = self.click.get()
        dicts['ms'] = self.ms.get()
        dicts['run_p1'] = self.run_p1.get()
        dicts['run_p2'] = self.run_p2.get()
        dicts['run_p3'] = self.run_p3.get()
        dicts['run_bfb1'] = re.sub('\D', '', self.run_bfb1.get())
        dicts['run_bfb2'] = re.sub('\D', '', self.run_bfb2.get())
        dicts['run_bfb3'] = re.sub('\D', '', self.run_bfb3.get())
        dicts['crash_is'] = self.crash_is.get()
        for k, v in dicts.items():
            if v.strip() == '':
                tkinter.messagebox.showinfo("提示", '{}不能为空'.format(k))
                break
                # raise NameError('{}不能为空'.format(k))
        monkey.runmonkey(dicts)

    # 运行计时
    def runtime(self):
        Label(self.root, text=datetime.datetime.now().strftime('%H:%M:%S')).place(x=90, y=450)
        while True:
            starttime = time.time()
            print('----------------------------------------------------------')
            print('开始计时')
            while True:
                times = round(time.time() - starttime, 0)
                time.sleep(1)
                Label(self.root, text=times).place(x=90, y=490)
                if monkey.rune_state is False:
                    print('退出计时')
                    Label(self.root, text=datetime.datetime.now().strftime('%H:%M:%S')).place(x=90, y=470)
                    break
            break

    def inster_data(self):
        logs = log_analysis.read_file().get_file()
        if logs:
            for i in range(len(logs)):
                # 给表格中添加数据
                self.tree_date.insert('', 1, text=logs[i][3], values=(logs[i][0], logs[i][1], logs[i][2]))
        else:
            print('没有收集到异常日志')
            self.tree_date.insert('', 1, text='未收集到异常日志', values=())

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
