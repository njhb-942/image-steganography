import sys
import tkinter
import encoder
import ttkbootstrap as ttk
import tkinter.messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog

global change, path


class myStdout():  # 重定向类
    def __init__(self):
        # 将其备份
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        t.insert('end', info)  # 在多行文本控件最后一行插入print信息
        t.update()  # 更新显示的文本，不加这句插入的信息无法显示
        t.see(tkinter.END)  # 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak


def btn_func():
    """Encode按键的触发事件"""
    global change,path
    print("设置的隐写程度超参数为：" + str(change) + "\n" +
          "******************************************************************************************************\n")

    print("选择写入文件路径为：" + path + "\n" +
          "******************************************************************************************************\n")

    # 此处引入主程序接口
    encoder.main(change=change,original_fileName=path)
    tkinter.messagebox.showinfo(message="加密成功")

def exit_func():
    """Exit按键的触发事件"""
    sys.exit()


def get_parameter():
    global change
    change = e1.get()


def get_path():
    """注意，以下列出的方法都是返回字符串而不是数据流"""
    # 返回一个字符串，且只能获取文件夹路径，不能获取文件的路径。
    # path = filedialog.askdirectory(title='请选择一个目录')

    # 返回一个字符串，可以获取到任意文件的路径。
    global path
    path = filedialog.askopenfilename(title='请选择文件')
    # 生成保存文件的对话框， 选择的是一个文件而不是一个文件夹，返回一个字符串。
    # path = filedialog.asksaveasfilename(title='请输入保存的路径')

    entry_text.set(path)

change = 3
path = "secret.py"
mystd = myStdout()  # 实例化重定向类

# window = tkinter.Tk()  # 实例化tk对象
# 套皮肤ttk
# 创建窗口
window = ttk.Window(
        title="图片隐写————加密程序",        #设置窗口的标题
        themename="vapor",     #设置主题
        size=(606,606),        #窗口的大小
        position=(300,200),     #窗口所在的位置
        minsize=(0,0),          #窗口的最小宽高
        maxsize=(735,685),    #窗口的最大宽高
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
lf1 = ttk.Labelframe(text="Encoder",bootstyle=PRIMARY,width=800,height=530)
lf1.pack()
# t = tkinter.Text(window)  # 创建多行文本控件
# 进度文本框
t=ScrolledText(lf1, padding=5, height=22, autohide=True)
t.pack()  # 布局在窗体上
t.insert(END, "********************************************加密准备就绪********************************************\n")
t.insert(END,"写入文件路径默认为本目录的secret.py\n")
t.insert(END,"隐写程度超参数默认为3\n")
t.insert(END, "*******************************************************************************************************\n")
# 路径选择组件
lf2 = ttk.Labelframe(text="Dir", bootstyle=PRIMARY, width=800, height=80)
lf2.pack(side=TOP, padx=5, pady=10)
lf2.pack_propagate(0)
label1 = tkinter.Label(lf2, text='选择写入文件：', font=("微软雅黑",15))
label1.pack(side=LEFT, padx=5, pady=10)
entry_text = tkinter.StringVar()
entry = ttk.Entry(lf2, textvariable=entry_text, font=('微软雅黑', 10), width=42, state='readonly')
entry.pack(side=LEFT, padx=5, pady=10)
button1 = tkinter.Button(lf2, text='选择路径', command=get_path)
button1.pack(side=RIGHT,padx=5, pady=10)


# 超参数选择组件
lf3 = ttk.Labelframe(text="Parameter",bootstyle=PRIMARY)
lf3.pack(side=LEFT, padx=5, pady=10)
label2 = tkinter.Label(lf3, text='选择隐写程度超参数：', font=("微软雅黑",15))
label2.pack(side=LEFT, padx=5, pady=10)
e1 = ttk.Entry(lf3, show=None)
e1.insert('0', "3")
e1.pack(side=LEFT, padx=5, pady=10)
button2 = tkinter.Button(lf3, text='修改', command=get_parameter)
button2.pack(side=RIGHT,padx=5, pady=10)

# 功能按钮组件
lf4 = ttk.Labelframe(text="Do", bootstyle=PRIMARY, width=170, height=79)
lf4.pack(side=RIGHT,padx=5, pady=10)
lf4.pack_propagate(0)
b1 = ttk.Button(lf4, text="Exit", bootstyle=(DANGER, "outline-toolbutton"), command=exit_func).pack(side=RIGHT, padx=5, pady=10)
b2 = ttk.Button(lf4, text="Encode", bootstyle=(LIGHT, "outline-toolbutton"), command=btn_func).pack(side=RIGHT, padx=5, pady=10)
# b = tkinter.Button(window, text='Encode', font=('Arial', 12), width=20, height=1,bg="light" ,command=btn_func)  # 创建按钮控件，并绑定触发事件
# b.pack()  # 布局在窗体上

window.mainloop()  # 显示窗体
mystd.restoreStd()  # 恢复标准输出

