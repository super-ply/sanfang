# -*- coding:utf-8 -*-
import os
import sys

sys.path.append("..")
import tkinter
import time
from tkinter import END
from tkinter import messagebox
from tkinter import scrolledtext
from appdownload.mi import *
from appdownload.miby import *
from appdownload.apkpureby import *
from appdownload.apkcomboby import *
from appdownload.apkpure import *
import threading
from appdownload.apkcombo import *
from appdownload.apkfollow import *
from appdownload.huawei import *
from appdownload.huaweiby import *

MiDownload = MiDownload()
MiBy = MiBy()
ApkPure = ApkPure()
ApkPureBy = ApkPureBy()
ApkComboBy = ApkComboBy()
ApkFollowBy = ApkFollowBy()
huaweiby = huaweiby()


class InitView:
    def __init__(self):
        win = tkinter.Tk()
        win.title("应用商店APK下载工具")
        win.geometry('500x300+1000+500')
        labelroot = tkinter.Label(win, fg='black')
        labelroot.place(relx=0.5, rely=0.5)
        M = tkinter.Menu(win)
        menubar = tkinter.Menu(win)
        scr = scrolledtext.ScrolledText(win, width=65, height=16,
                                        font=("微软雅黑", 10, "bold"))  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        scr.place(x=0, y=0)

        def printLog():
            threading.Thread(target=threadToUpdate).start()

        def threadToUpdate():
            if os.path.exists('..\\log\\runtime.log'):
                log = open('..\\log\\runtime.log', 'r')
                line = log.readline()
                while line:
                    scr.insert(END, line)
                    line = log.readline()
                    scr.see(END)

        content = [['huaweiTop应用下载', 'huawei按照包名下载'], ['miTop应用下载', 'mi按照包名下载'], ['APKPureTop下载', 'APKPure按照包名下载'],
                   ['APKComboTop下载', 'APKCombo按包名下载'], ['APKFollow按照包名下载'], ['刷新日志'], ['版本信息']]
        Main = ['华为', '小米商店', '外销', '运行日志', '关于']
        for i in range(len(Main)):
            # 新建一个空的菜单,将menubar的menu属性指定为filemenu，即filemenu为menubar的下拉菜单
            filemenu = tkinter.Menu(menubar, tearoff=0)
            for sonmenu in content[i]:
                if sonmenu == "miTop应用下载":
                    filemenu.add_command(label=sonmenu, command=self.Mi_toast)
                elif sonmenu == "mi按照包名下载":
                    filemenu.add_command(label=sonmenu, command=self.Mi_toast_package)
                elif sonmenu == "huaweiTop应用下载":
                    filemenu.add_command(label=sonmenu, command=self.huawei_toast)
                elif sonmenu == "huawei按照包名下载":
                    filemenu.add_command(label=sonmenu, command=self.huawei_toast_package)
                elif sonmenu == "版本信息":
                    filemenu.add_command(label=sonmenu, command=self.about)
                elif sonmenu == "刷新日志":
                    filemenu.add_command(label=sonmenu, command=printLog)
                elif sonmenu == "APKPureTop下载":
                    filemenu.add_command(label=sonmenu, command=self.ApkPure_toast)
                elif sonmenu == "APKPure按照包名下载":
                    filemenu.add_command(label=sonmenu, command=self.Apk_toast_package)
                elif sonmenu == "APKComboTop下载":
                    filemenu.add_command(label=sonmenu, command=self.Apkcombo_toast)
                elif sonmenu == "APKCombo按包名下载":
                    filemenu.add_command(label=sonmenu, command=self.ApkCombo_toast_package)
                elif sonmenu == "APKFollow按照包名下载":
                    filemenu.add_command(label=sonmenu, command=self.ApkFollow_toast_package)
                else:
                    filemenu.add_command(label=sonmenu)
            menubar.add_cascade(label=Main[i], menu=filemenu)
        win['menu'] = menubar
        printLog()
        win.mainloop()

    def MiTopDownload(self, nums=10):
        threading.Thread(target=MiDownload.craw_apks, args=(nums,)).start()

    def MiDownloadByPackageName(self):
        threading.Thread(target=MiBy.getDownLoadUrl).start()

    def HuaweiTopDownload(self, nums=2):
        threading.Thread(target=huaweiby.download_apk, args=(nums,)).start()

    def HuaweiDownloadByPackageName(self):
        threading.Thread(target=huaweiby.downloadApps).start()

    def ApkPureDownloadByPackageName(self):
        threading.Thread(target=ApkPureBy.getDownLoadUrl).start()

    def ApkComboTopDownload(self, nums):
        threading.Thread(target=apkcombo_by.download_apk, args=(nums,)).start()

    def ApkComboDownloadPackageName(self):
        threading.Thread(target=ApkComboBy.getDownLoadUrl).start()

    def ApkFollowDownloadPackageName(self):
        threading.Thread(target=ApkFollowBy.getDownLoadUrl).start()

    def killPython(self):
        pass

    def ApkPureTopDownload(self, nums=10):
        threading.Thread(target=ApkPure.craw_apks, args=(nums,)).start()

    def about(self):
        messagebox.showinfo('信息', '版本:v1.0\n' +
                            '研发团队:AutoMation')

    def Apkcombo_toast_package(self, nums=3):
        threading.Thread(target=apkcombo_by.download_apk(nums)).start()

    def ApkCombo_toast_package(self):
        messagebox.showwarning('警告', '需要保存apkcombo.txt在config文件夹内')
        try:
            self.ApkComboDownloadPackageName()
        except:
            messagebox.showwarning('错误', '未预置apkcombo.txt在config文件夹内')

    def ApkFollow_toast_package(self):
        messagebox.showwarning('警告', '需要保存apkfollow.txt在config文件夹内')
        try:
            self.ApkFollowDownloadPackageName()
        except:
            messagebox.showwarning('错误', '未预置apkfollow.txt在config文件夹内')

    def huawei_toast_package(self):
        messagebox.showwarning('警告', '需要保存huawei.txt在config文件夹内')
        try:
            self.HuaweiDownloadByPackageName()
        except:
            messagebox.showwarning('错误', '未预置huawei.txt在config文件夹内')

    def huawei_toast(self):
        def getInput():
            app_nums = entry1.get()  # 获取文本框的内容
            self.HuaweiTopDownload(int(app_nums))
            messagebox.showinfo('提示', '正在下载TOP' + app_nums + 'APK，下载路径为当前应用路径apk文件夹')

        c = tkinter.Tk()
        c.geometry('300x90+850+350')
        c.title("输入下载TOP数量")
        entry1 = tkinter.Entry(c, width=20)
        entry1.pack()
        button = tkinter.Button(c, text="下载", command=getInput)  # 收到消息执行这个函数
        button.pack()
        c.mainloop()

    def ApkPure_toast(self):
        def getInput():
            app_nums = new_entry.get()  # 获取文本框的内容
            self.ApkPureTopDownload(int(app_nums))
            messagebox.showinfo('提示', '正在下载TOP' + app_nums + 'APK，下载路径为当前应用路径apk文件夹')

        b = tkinter.Tk()
        b.title("输入下载TOP数量")
        b.geometry('300x90+850+350')
        new_entry = tkinter.Entry(b, width=20)
        new_entry.pack()
        button = tkinter.Button(b, text="下载", command=getInput)  # 收到消息执行这个函数
        button.pack()
        b.mainloop()

    def Apkcombo_toast(self):
        def getInput():
            app_nums = entry1.get()  # 获取文本框的内容
            self.ApkComboTopDownload(int(app_nums))
            messagebox.showinfo('提示', '正在下载TOP' + app_nums + 'APK，下载路径为当前应用路径apk文件夹')

        d = tkinter.Tk()
        d.geometry('300x90+850+350')
        d.title("输入下载TOP数量")
        entry1 = tkinter.Entry(d, width=20)
        entry1.pack()
        button = tkinter.Button(d, text="下载", command=getInput)  # 收到消息执行这个函数
        button.pack()
        d.mainloop()

    def Mi_toast(self):
        def getInput():
            app_nums = entry1.get()  # 获取文本框的内容
            self.MiTopDownload(int(app_nums))
            messagebox.showinfo('提示', '正在下载TOP' + app_nums + 'APK，下载路径为当前应用路径apk文件夹')

        a = tkinter.Tk()
        a.geometry('300x90+850+350')
        a.title("输入下载TOP数量")
        entry1 = tkinter.Entry(a, width=20)
        entry1.pack()
        button = tkinter.Button(a, text="下载", command=getInput)  # 收到消息执行这个函数
        button.pack()
        a.mainloop()

    def Mi_toast_package(self):
        messagebox.showwarning('警告', '需要保存mi.txt在config文件夹内')
        try:
            self.MiDownloadByPackageName()
        except:
            messagebox.showwarning('错误', '未预置mi.txt在config文件夹内')

    def Apk_toast_package(self):
        messagebox.showwarning('警告', '需要保存未预置apkpure.txt在config文件夹内')
        try:
            self.ApkPureDownloadByPackageName()
        except:
            messagebox.showwarning('错误', '未预置apkpure.txt在config文件夹内')


InitView = InitView()
