#coding=utf-8
import logging
import requests
import re
import urllib
import sys
sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

_root_url="https://apkpure.com" #/cn/search?q=com.android.vending

class ApkPureBy:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('APKPUREBYNAME'+PhoneUtil.getTodayData(self))
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def getAppPages(self):
        app_lists = self.getAppList()
        app_pages = []
        for appname in app_lists:
            app_page = "https://apkpure.com/cn/search?q="+appname  #Mi商店搜索下载规则
            app_pages.append(app_page)
        return app_pages


    def getAppList(self):
        app_lists = []
        apptxt = open("..\\config\\apkpure.txt", 'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line = apptxt.readline()
        apptxt.close()
        return app_lists

    def getDownLoadUrl(self, path="..\\apk\\"):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        data = PhoneUtil.getTodayData(self)
        apk_address = path+'ApkPureByName'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        urls = self.getAppPages()
        for url in urls:
            wbdata = requests.get(url, self.header).text
            soup = BeautifulSoup(wbdata, "html.parser")
            try:
                download_link = soup.find(class_="more-down")["href"]
                download_url = urllib.parse.urljoin(_root_url, str(download_link))
                packagename = (download_link.split('/'))[3]
                downurl_data = requests.get(download_url, self.header).text
                soup_two = BeautifulSoup(downurl_data, "html.parser")
                download_link_page = soup_two.find(class_=" da")["href"]
                download_page = urllib.parse.urljoin(_root_url, str(download_link_page))
                app_data = download_page+'/download?from=details'
                detail_data = requests.get(app_data, headers=self.header).text
                soup_third = BeautifulSoup(detail_data, "html.parser")
                download = soup_third.find(id="download_link")["href"]
                print("download"+download)
                #self.logger.info("正在下载应用: "+packagename)
                urllib.request.urlretrieve(download, apk_address+packagename+'.apk')
            except:
                self.logger.info("异常app网页/网络异常"+str(packagename))

if __name__=="__main__":
    ApkPureBy = ApkPureBy()
    print(ApkPureBy.getDownLoadUrl())