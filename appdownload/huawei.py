# -*- coding: UTF-8 -*-
import logging
from bs4 import BeautifulSoup
import requests
import urllib.request
from utils.utils import PhoneUtil

class huaweiby:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('MIBYNAME'+PhoneUtil.getTodayData(self))

    def getName(self):
        applist = []
        f = open('..\\config\\huawei.txt', 'r')
        for lines in f.readlines():
            line = lines.strip("\n")
            applist.append(line)
        f.close()
        print(applist)
        return applist

    def downloadApps(self):
        '''华为应用市场'''
        data = {'some': 'data'}
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        _root_url = "https://appstore.huawei.com/"  # 应用市场主页网址
        save_path = "..\\apk\\"
        date = PhoneUtil.getTodayData(self)
        apk_address = save_path + "huawei" + date + "\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        names = self.getName()
        for name in names:
            downloadurl = "https://appstore.huawei.com/search/" + str(name) #单个apk下载地址
            wbdata = requests.get(downloadurl, headers=headers).text  #网页内容
            soup = BeautifulSoup(wbdata, "html.parser")
            links = soup.find_all('a', attrs={"class": "btn-blue down"})  #获取当前页所有apk下载链接
            apklist = []   #apk下载链接列表
            for item in links:
                apk = str(item).split(",")[5].strip("'")
                apklist.append(apk)
            firstapk = apklist[0]
            apkname = str(firstapk).split('/')[9]
            realapkname = str(apkname).split('?')[0]  #俩段截取获得apk包名
            print(realapkname)
            try:
                urllib.request.urlretrieve(firstapk, apk_address+realapkname)
                self.logger.info("下载完成")
            except Exception as e:
                print("fail:" + str(e))

    def saveApks(self):
        pass

if __name__ == "__main__":
    app = huaweiby()
    app.downloadApps()
