# encoding: utf8
# usage: 简单的对话框窗口设计

from tkinter import * # pythonGUI库, 用于简单的对话框生成
from tkinter import ttk # 尝试使用ttk风格控件
from tkinter import messagebox # 消息框
import num_check # 功能的后端实现

def main():
    """前端窗口的主要函数"""

    # 定义主要功能
    def judge_even():
        """判断一个数是否为偶数的前端函数"""
        num_in_str = entry.get()
        try:
            num_in_int = int(num_in_str)
        except:
            messagebox.showerror(title="判断奇偶性", message="输入有误，请重试！")
            entry.delete(0, END) # 删除文本框内所有文本
        else:
            if num_check.is_even(num_in_int):
                messagebox.showinfo(title="判断奇偶性", message=f"输入的数字是偶数")
            else:
                messagebox.showinfo(title="判断奇偶性", message=f"输入的数字是奇数")
        finally:
            pass

    def judge_prime():
        """判断一个数是否为素数的前端函数"""
        num_in_str = entry.get()
        try:
            num_in_int = int(num_in_str)
        except:
            messagebox.showerror(title="判断素数", message="输入有误，请重试！")
            entry.delete(0, END) # 删除文本框内所有文本
        else:
            if num_check.is_prime(num_in_int):
                messagebox.showinfo(title="判断素数", message=f"输入的数字是素数")
            else:
                messagebox.showinfo(title="判断素数", message=f"输入的数字是合数")
        finally:
            pass

    def find_nearest_prime():
        """寻找距离一个数最近的素数"""
        num_in_str = entry.get()
        try:
            num_in_int = int(num_in_str)
        except:
            messagebox.showerror(title="寻找素数", message="输入有误，请重试！")
            entry.delete(0, END) # 删除文本框内所有文本
        else:
            find_res = num_check.find_nearest_prime(num_in_int)
            if len(find_res) == 1:
                messagebox.showinfo(title="寻找素数", message=f"离{num_in_int}最近的素数是{find_res[0]}")
            elif len(find_res) == 2:
                messagebox.showinfo(title="寻找素数", message=f"离{num_in_int}最近的素数是{find_res[0]}和{find_res[1]}")
            else:
                messagebox.showerror(title="寻找素数", message="程序运行出现错误")
        finally:
            pass
    
    def ask_quit():
        """询问是否退出的前端函数"""
        is_quit = messagebox.askyesno(title="提示", message="您确定要退出吗？")
        if is_quit:
            root.destroy()

    # 定义主要控件
    root = Tk(className="数字性质判定")
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    label = ttk.Label(frm, text="请输出需要判定性质的数字")
    label.grid(column=0, row=0)
    entry = ttk.Entry(frm, width=50)
    entry.grid(column=0, row=1)
    even_button = ttk.Button(frm, text="判断奇偶性", command=judge_even)
    even_button.grid(column=0, row=2)
    prime_button = ttk.Button(frm, text="判断素数", command=judge_prime)
    prime_button.grid(column=0, row=3)
    find_button = ttk.Button(frm, text="寻找素数", command=find_nearest_prime)
    find_button.grid(column=0, row=4)
    exit_button = ttk.Button(frm, text="退出", command=ask_quit)
    exit_button.grid(column=0, row=5)
    root.mainloop()

if __name__ == "__main__":
    main()