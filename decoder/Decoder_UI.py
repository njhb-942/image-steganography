import sys
import tkinter
import decoder
import ttkbootstrap as ttk
import tkinter.messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

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
    """Decode按键的触发事件"""
    # 此处引入主程序接口
    decoder.main()
    tkinter.messagebox.showinfo(message="解密成功")

def exit_func():
    """Exit按键的触发事件"""
    sys.exit()



mystd = myStdout()  # 实例化重定向类

# window = tkinter.Tk()  # 实例化tk对象
# 套皮肤ttk
window = ttk.Window(
        title="图片隐写————解密程序",        #设置窗口的标题
        themename="vapor",     #设置主题
        size=(606,526),        #窗口的大小
        position=(300,200),     #窗口所在的位置
        minsize=(0,0),          #窗口的最小宽高
        maxsize=(735,585),    #窗口的最大宽高
        resizable=None,         #设置窗口是否可以更改大小
        alpha=0.9,              #设置窗口的透明度(0.0完全透明）
        )
lf1 = ttk.Labelframe(text="Decoder",bootstyle=PRIMARY,width=800,height=530)
lf1.pack()
# t = tkinter.Text(window)  # 创建多行文本控件
# 进度文本框
t=ScrolledText(lf1, padding=5, height=22, autohide=True)
t.pack()  # 布局在窗体上
t.insert(END, "********************************************解密准备就绪********************************************\n")
# 功能按钮组件
lf2 = ttk.Labelframe(text="Do", bootstyle=PRIMARY, width=709, height=79)
lf2.pack(side=TOP,padx=5, pady=10)
lf2.pack_propagate(0)
label1 = tkinter.Label(lf2, text='请将载秘图片放入本目录/out下', font=("微软雅黑",15))
label1.pack(side=LEFT, padx=5, pady=10)
b1 = ttk.Button(lf2, text="Exit", bootstyle=(DANGER, "outline-toolbutton"), command=exit_func).pack(side=RIGHT, padx=5, pady=10)
b2 = ttk.Button(lf2, text="Decode", bootstyle=(LIGHT, "outline-toolbutton"), command=btn_func).pack(side=RIGHT, padx=5, pady=10)
# b = tkinter.Button(window, text='Encode', font=('Arial', 12), width=20, height=1,bg="light" ,command=btn_func)  # 创建按钮控件，并绑定触发事件
# b.pack()  # 布局在窗体上

window.mainloop()  # 显示窗体
mystd.restoreStd()  # 恢复标准输出

