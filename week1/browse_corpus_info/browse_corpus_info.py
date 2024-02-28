# encoding: utf8
# usage: 对应的GUI文件

import tkinter # PythonUI库
from tkinter import ttk # 美化版UI库
from tkinter import messagebox # 信息框库
from tkinter import filedialog # 文件选择对话框
import corpus_info_backend as backend # 后端文件

def main():
    # 主要功能函数
    def get_size():
        """获知文件夹内容和文件大小的前端函数"""
        root_dir = filedialog.askdirectory(mustexist=True, title="选择要获知的文件夹")
        # 执行后端程序
        backend.get_root_size(root_dir)
        # 报告信息
        messagebox.showinfo(title="提示", message=f"文件夹{root_dir}下内容已统计完毕。详见{backend.size_file()}文件")

    def add_fix():
        """批量添加文件名前缀后缀"""

        def add_prefix():
            change = messagebox.askyesno(title='提示', message='更名操作不可逆！确定更名吗？')
            if change:
                backend.modify_paths(root_dir, entry.get(), 'prefix')
                window.destroy()

        def add_suffix():
            change = messagebox.askyesno(title='提示', message='更名操作不可逆！确定更名吗？')
            if change:
                backend.modify_paths(root_dir, entry.get(), 'suffix')
                window.destroy()

        # 选择要更名的文件夹
        root_dir = filedialog.askdirectory(mustexist=True, title="选择要获知的文件夹")
        # 增加窗口收集信息
        window = tkinter.Tk(className="添加文件名前缀后缀")
        frm1 = ttk.Frame(window, padding=100)
        frm1.grid()
        label = ttk.Label(frm1, text="请填写要在文件名中添加的文字")
        entry = ttk.Entry(frm1)
        entry.grid(column=0, row=1)
        prefix_button = ttk.Button(frm1, text="添加为前缀", command=add_prefix)
        prefix_button.grid(column=0, row=2)
        suffix_button = ttk.Button(frm1, text="添加为后缀", command=add_suffix)
        suffix_button.grid(column=0, row=3)
    
    def safe_exit():
        """退出程序函数"""
        is_quit = messagebox.askyesno(title="提示", message="确定要退出吗？")
        if is_quit:
            root.destroy()
    
    # 窗口部件
    root = tkinter.Tk(className="文件信息获得与文件更名")
    # 框架部件
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    # 按钮配件
    get_size_button = ttk.Button(frm, text="获知文件夹内容", command=get_size)
    get_size_button.grid(column=0, row=0)
    modify_name_button = ttk.Button(frm, text="修改文件内容", command=add_fix)
    modify_name_button.grid(column=0, row=1)
    exit_button = ttk.Button(frm, text="退出", command=safe_exit)
    exit_button.grid(column=0, row=2)
    root.mainloop()

if __name__ == "__main__":
    main()