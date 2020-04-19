# coding=utf-8
import logging
from urllib.request import urlopen
import requests
import re
import urllib
import sys
import time
import bs4
sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

_root_url = "https://apkcombo.com/zh-ru/category/app/"


class ApkComboBy:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('APKPUREBYNAME' + PhoneUtil.getTodayData(self))
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def getAppPages(self):
        app_lists = self.getAppList()
        app_pages = []
        for appname in app_lists:
            app_page = "https://apkcombo.com/zh-ru/search?q=" + appname
            app_pages.append(app_page)
        return app_pages

    def getAppList(self):
        app_lists = []
        apptxt = open("..\\config\\apkcombo.txt", 'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line = apptxt.readline()
        apptxt.close()
        return app_lists

    def getDownLoadUrl(self, path="..\\apk\\"):
        originurl = 'https://apkcombo.com'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        data = PhoneUtil.getTodayData(self)
        apk_address = path + 'ApkComboByName' + data + "\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        urls = self.getAppList()
        for url in urls:
            webdata = urlopen(url).read().decode('utf-8')
            #webdata = requests.get(url).text
            soup = BeautifulSoup(webdata, "html.parser")
            download_links = soup.find_all('a', href=re.compile("/download/apk"))
            download_link = str(download_links).split("\"")[3]
            allLink = str(originurl) + str(download_link)
            newWbdata = urlopen(allLink).read().decode('utf-8')
            time.sleep(10)
            soup = BeautifulSoup(newWbdata, "html.parser")
            print(soup)
            downloadlinks = soup.find(class_="app")["href"]
            print(downloadlinks)
            packagename = str(allLink).split('/')[4]
            self.logger.info("正在下载应用: "+packagename)
            try:
                urllib.request.urlretrieve(downloadlinks, apk_address + packagename + '.apk')
                self.logger.info("下载完成")
            except:
                self.logger.info("异常app网页/网络异常" + str(packagename))

if __name__ == "__main__":
    ApkComboBy = ApkComboBy()
    ApkComboBy.getDownLoadUrl()