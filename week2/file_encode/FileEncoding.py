# encoding: utf8
# usage: 程序前端

# GUI库
import tkinter
from tkinter import ttk, messagebox, filedialog
# 后端文件
import pinyin_seq as seq
import encoding_functions as efunc
import file_encoding_transfer as ftrans

def main():
    """程序运行主函数
    """
    # 功能函数
    def char2en_func():
        """由文字查编码
        """
        def query():
            # 取输入框中的文本执行查询
            en_dict = efunc.char_to_encoding(char_entry.get())
            # 按格式输出(注意下述式子定义的格式)
            output_info = f"汉字{char_entry.get()}的编码值为:\n"
            output_info += "".join([f"{i}: {en_dict[i]}\n" for i in en_dict])
            messagebox.showinfo(title="查询结果", message=output_info)

        char2en_top = tkinter.Toplevel(root)
        frm = ttk.Frame(char2en_top, padding=200)
        frm.grid()
        char_label = ttk.Label(frm, text='请输入要查询的汉字')
        char_label.grid(column=0, row=0)
        char_entry = ttk.Entry(frm)
        char_entry.grid(column=0, row=1)
        char_exe = ttk.Button(frm, text="查询", command=query)
        char_exe.grid(column=0, row=2)
    
    def en2char_func():
        """由编码查文字
        """
        def query():
            char = efunc.encoding_to_char(en_menu.get(), en_entry.get())
            if char:
                messagebox.showinfo(title="查询结果", message=f"编码集: {en_menu.get()}, 编码:{en_entry.get()}, 汉字:{char}")
            else:
                messagebox.showerror(title="查询结果", message="未查出结果！")
        
        en2char_top = tkinter.Toplevel(root)
        frm = ttk.Frame(en2char_top, padding=200)
        frm.grid()
        en_label = ttk.Label(frm, text="请输入16进制编码, 选择编码集")
        en_label.grid(column=0, row=0)
        en_entry = ttk.Entry(frm)
        en_entry.grid(column=0, row=1)
        en_menu = ttk.Combobox(frm, textvariable=tkinter.StringVar())
        en_menu['value'] = efunc.ENCODING_TYPES
        en_menu.grid(column=1, row=1)
        en_button = ttk.Button(frm, text='查询', command=query)
        en_button.grid(column=0, row=2)
    
    def trans_func():
        src_dir = filedialog.askdirectory(title="选择需要转换编码文件所在的文件夹")
        dst_dir = filedialog.askdirectory(title="选择转换编码后文件放置的文件夹")
        ftrans.dir_transfer(src_dir, dst_dir)
        messagebox.showinfo(title="提示", message=f"文件编码转换完成, 请查看{dst_dir}文件夹")
    
    def pinyin_output_func():
        def query():
            pinyin = seq.pinyin_query(entry.get())
            if pinyin:
                messagebox.showinfo(title="结果", message=f"汉字{entry.get()}的拼音为"+", ".join(pinyin))
            else:
                messagebox.showerror(title="结果", message=f"汉字{entry.get()}的拼音无法查询")

        top = tkinter.Toplevel(root)
        frm = ttk.Frame(top, padding=200)
        frm.grid()
        label = ttk.Label(frm, text="请输入汉字")
        label.grid(column=0, row=0)
        entry = ttk.Entry(frm)
        entry.grid(column=0, row=1)
        button = ttk.Button(frm, text="查询", command=query)
        button.grid(column=0, row=2)

    def pinyin_sort_func():
        def sort():
            sorted_chars = seq.pinyin_sort([c for c in entry.get()])
            if sorted_chars:
                messagebox.showinfo(title="结果", message="汉字的音序为" + ", ".join(sorted_chars))
            else:
                messagebox.showerror(title="结果", message="由于拼音无法查询, 排序失败")

        top = tkinter.Toplevel(root)
        frm = ttk.Frame(top, padding=200)
        frm.grid()
        label = ttk.Label(frm, text="请输入需要排序的汉字, 中间无需间隔符号")
        label.grid(column=0, row=0)
        entry = ttk.Entry(frm)
        entry.grid(column=0, row=1)
        button = ttk.Button(frm, text="排序", command=sort)
        button.grid(column=0, row=2)
    
    # 主要控件
    root = tkinter.Tk(className="编码与拼音小工具")
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    # 编码小工具控件
    encoding_label = ttk.Label(frm, text='编码小工具')
    encoding_label.grid(column=0, row=0)
    char2en = ttk.Button(frm, text="由汉字查码值", command=char2en_func)
    char2en.grid(column=1, row=0)
    en2char = ttk.Button(frm, text="由码值查汉字", command=en2char_func)
    en2char.grid(column=2, row=0)
    # 转码小工具控件
    transfer_label = ttk.Label(frm, text='转码小工具')
    transfer_label.grid(column=0, row=1)
    char_trans = ttk.Button(frm, text="文件格式及编码转换", command=trans_func)
    char_trans.grid(column=1, row=1)
    # 拼音小工具控件
    pinyin_label = ttk.Label(frm, text='拼音小工具')
    pinyin_label.grid(column=0, row=2)
    pinyin_output = ttk.Button(frm, text="输出拼音", command=pinyin_output_func)
    pinyin_output.grid(column=1, row=2)
    pinyin_sort = ttk.Button(frm, text="汉字音序", command=pinyin_sort_func)
    pinyin_sort.grid(column=2, row=2)

    root.mainloop()

if __name__ == "__main__":
    main()