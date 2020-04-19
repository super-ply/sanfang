# coding=utf-8
import logging
from urllib.request import urlopen
import re
import urllib
import sys

sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

_root_url = "https://www.apkfollow.com/search?q="

class ApkFollowBy:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('APKPUREBYNAME' + PhoneUtil.getTodayData(self))
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def getAppPages(self):
        app_lists = self.getAppList()
        app_pages = []
        for appname in app_lists:
            app_page = "https://www.apkfollow.com/search?q=" + appname
            app_pages.append(app_page)
        return app_pages

    def getAppList(self):
        app_lists = []
        apptxt = open("..\\config\\apkfollow.txt", 'r')
        line = apptxt.readline()
        while line:
            if len(line) > 0:
                line = line.strip("\n")
                app_lists.append(line)
            line = apptxt.readline()
        apptxt.close()
        return app_lists

    def getDownLoadUrl(self, path="..\\apk\\"):
        originurl = 'https://www.apkfollow.com'
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        data = PhoneUtil.getTodayData(self)
        apk_address = path + 'ApkfollowByName' + data + "\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        urls = self.getAppPages()
        for url in urls:
            print(url)
            print("**************************************************************")
            wbdata = urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(wbdata, "html.parser")
            download_links = soup.find_all('a', href=re.compile("/app/"))
            download_link = originurl + str(download_links).split("\"")[1]
            newWbdata = urlopen(download_link).read().decode('utf-8')
            soup = BeautifulSoup(newWbdata, "html.parser")
            allLinks = soup.find_all(id='download-btn')
            downloadlinks = str(allLinks).split('\"')[3].strip("#").strip("$")
            packagename = str(downloadlinks).split('_')[2]
            print(packagename)
            realDownloadLink = originurl + downloadlinks
            self.logger.info("正在下载应用: "+packagename)
            try:
                urllib.request.urlretrieve(realDownloadLink, apk_address + packagename + '.apk')
                self.logger.info("下载完成")
            except:
                self.logger.info("异常app网页/网络异常")




if __name__ == "__main__":
    ApkFollowBy = ApkFollowBy()
    ApkFollowBy.getDownLoadUrl()