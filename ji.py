import tkinter

root = tkinter.Tk()


# 增加背景图片
photo = tkinter.PhotoImage(file="img.png")
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

tkinter.mainloop()