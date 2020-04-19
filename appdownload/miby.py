#coding=utf-8
import logging
import requests
import re
import urllib
import sys
sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

_root_url = "http://app.mi.com"

class MiBy:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('MIBYNAME'+PhoneUtil.getTodayData(self))
       
    def getAppPages(self):
        app_lists = self.getAppList()
        app_pages = []
        for appname in app_lists:
            app_page = "http://app.mi.com/details?id="+appname+"&ref=search"  #Mi商店搜索下载规则
            app_pages.append(app_page)
        return app_pages


    def getAppList(self):
        app_lists = []
        apptxt = open("..\\config\\mi.txt",'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line = apptxt.readline()
        apptxt.close()
        return app_lists

    def getDownLoadUrl(self, path="..\\apk\\"):
        data = PhoneUtil.getTodayData(self)
        apk_address = path+'MiByName'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        urls = self.getAppPages()
        for url in urls:
            wbdata = requests.get(url).text
            soup = BeautifulSoup(wbdata, "html.parser")
            try:
                download_link = soup.find(class_="download")["href"]
                download_url = urllib.parse.urljoin(_root_url, str(download_link))
                packagename = ((download_url.split('='))[1]).split('&')[0]
                self.logger.info("正在下载应用: "+packagename)
                urllib.request.urlretrieve(download_url, apk_address+packagename+'.apk')
            except:
                self.logger.info("异常app网页"+str(packagename))

if __name__=="__main__":
    MiBy = MiBy()
    MiBy.getDownLoadUrl()