import os
import json
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

__version__ = "1.4"

content = ""
dic = {}

def chkfile():
    global content
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            content = file.read()
            
    else:
        file = open("contacts.json", "w")
        file.close()
        content = ""

def main():
    global content, dic
    win = Tk()
    win.resizable(0,0)
    win.geometry("+300+200")
    win.title("通讯录V1.4 -- By lanlan2_")
    win.iconbitmap("ct.ico")
    chkfile()
    fm1 = Frame(win)
    fm1.pack(fill=BOTH)
    fm2 = Frame(win)
    fm2.pack(pady=5)
    fm2_1 = Frame(fm2)
    fm2_2 = Frame(fm2)
    fm2_1.pack(side=LEFT, padx=10)
    fm2_2.pack(side=RIGHT, padx=10)
    fm3 = Frame(win)
    fm3.pack()
    tree = Treeview(fm1, columns=("people","telephone"), show="headings", selectmode="browse")
    tree.column("people", minwidth=100, width = 216)
    tree.column("telephone", minwidth=100, width = 216)
    tree.heading("people", text="联系人")
    tree.heading("telephone", text="电话号码")
    tree.grid(column=1, row=1, sticky="nwes")
    scroll = Scrollbar(fm1, orient="vertical", command=tree.yview)
    scroll.grid(column=2, row=1, sticky="nwes")
    tree.config(yscrollcommand=scroll.set)
    try:
        dic = json.loads(content)
    except json.decoder.JSONDecodeError:
        print(content)
        content = "{}"
        dic = json.loads(content)

    def update():
        global dic
        for item in tree.get_children():
            tree.delete(item)
        for key in dic:
            tree.insert("", END, values=(key, dic[key]))
        win.update()

    update()
    
    def add(index, value):
        dic[index] = value
        update()
        sel = []
        for child in tree.get_children():
            if index == str(tree.item(child)['values'][0]):
                sel.append(child)
        tree.see(sel)
        tree.update()
        with open("contacts.json", "w") as file:
            file.write(json.dumps(dic, sort_keys=True, indent=4))
            
    def delete(index):
        del dic[index]
        update()
        with open("contacts.json", "w") as file:
            file.write(json.dumps(dic, sort_keys=True, indent=4))
            
    def verify(index, value):
        if index not in dic:
            showinfo("提示", "由于要更改的联系人“%s”不存在，因此新创建了一位联系人" % index)
            add(index, value)
        else:
            dic[index] = value
            update()
            with open("contacts.json", "w") as file:
                file.write(json.dumps(dic, sort_keys=True, indent=4))
                
    def clear():
        global dic
        dic = {}
        update()
        with open("contacts.json", "w") as file:
            file.write(json.dumps(dic, sort_keys=True, indent=4))

    def searchx():
        ind = ent1.get()
        if ind.strip() == "":
            showwarning("警告","联系人不能为空！")
            return
        else:
            try:
                exp = dic[ind]
            except Exception:
                showerror("错误", "要搜索的联系人“%s”不存在!" % ind)
                return
            val = dic[ind]
            ent2.delete(0, END)
            ent2.insert(0, val)
            sel = []
            for child in tree.get_children():
                if ind == str(tree.item(child)['values'][0]):
                    sel.append(child)
            tree.selection_set(sel)
            tree.see(sel)
            win.update()
            showinfo("提示","联系人“%s”搜索成功！" % ind)
            

    def addx():
        ind = ent1.get()
        val = ent2.get()
        if ind.strip() == "" or val.strip() == "":
            showwarning("警告","联系人或电话号码不能为空！")
            return
        else:
            try:
                exp = int(val)
            except Exception:
                showerror("错误","您输入的不是电话号码！")
            else:
                if ind in dic:
                    showwarning("警告", "要新增的联系人“%s”已存在！" % ind)
                else:
                    add(ind, val)

    def deletex():
        ind = ent1.get()
        if ind.strip() == "":
            showwarning("警告","联系人不能为空！")
            return
        else:
            try:
                exp = dic[ind]
            except Exception:
                showerror("错误", "要删除的联系人“%s”不存在!" % ind)
                return
            ans = askyesno("提示", "您将要删除联系人“%s”，您确定要这么做吗？" % ind)
            if ans == True:
                delete(ind)
                ent1.delete(0, END)
                ent2.delete(0, END)

    def verifyx():
        ind = ent1.get()
        val = ent2.get()
        if ind.strip() == "" or val.strip() == "":
            showwarning("警告","联系人或电话号码不能为空！")
            return
        else:
            try:
                exp = int(val)
            except Exception:
                showerror("错误","您输入的不是电话号码！")
            else:
                verify(ind, val)

    def clearx():
        ans = askyesno("提示","您将要清空整个通讯录，您确定要这么做吗？")
        if ans == True:
            clear()
            ent1.delete(0, END)
            ent2.delete(0, END)
        

    lab1 = Label(fm2_1, text="联系人")
    lab1.grid(row=1, column=1)
    lab2 = Label(fm2_2, text="电话号码")
    lab2.grid(row=1, column=1)
    ent1 = Entry(fm2_1)
    ent1.grid(row=1, column=2)
    ent2 = Entry(fm2_2)
    ent2.grid(row=1, column=2)

    but1 = Button(fm3, text="搜索联系人", command=searchx)
    but1.grid(row=1, column=1, padx=1)
    but2 = Button(fm3, text="增加联系人", command=addx)
    but2.grid(row=1, column=2, padx=1)
    but3 = Button(fm3, text="删除联系人", command=deletex)
    but3.grid(row=1, column=3, padx=1)
    but4 = Button(fm3, text="更改联系人信息", command=verifyx)
    but4.grid(row=1, column=4, padx=1)
    but5 = Button(fm3, text="清空通讯录", command=clearx)
    but5.grid(row=1, column=5, padx=1)

    def changent(event):
        key, val =tree.item(tree.selection(), "values")
        ent1.delete(0, END)
        ent2.delete(0, END)
        ent1.insert(0, key)
        ent2.insert(0, val)
        win.update()

    tree.bind("<<TreeviewSelect>>", changent)
    win.mainloop()
    
if __name__ == "__main__":
    main()
