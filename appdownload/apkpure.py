#coding=utf-8
import logging
import requests
import sys
import re
import urllib
import time
sys.path.append("..")
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup
   
class ApkPure:
    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('APKPURETOP'+PhoneUtil.getTodayData(self))
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def parser_apks(self, count=1):
        '''apkpure'''
        #伪装浏览器
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        _root_url = 'https://apkpure.com'
        res_parser = {}
        page_num = 1 #设置爬取的页面，从第一页开始爬取，第一页爬完爬取第二页，以此类推
        while count:
            time.sleep(3)
            wbdata = requests.get("https://apkpure.com/cn/app?sort=download&page="+str(page_num), headers=self.header).text
            soup = BeautifulSoup(wbdata, "html.parser")
            download_links = soup.body.contents[9].find_all('a', href=re.compile("/download?"))  #当前页所有apk下载地址
            for download_link in download_links:
                download_link = download_link.get('href')  #单个apk下载地址
                detail_link = urllib.parse.urljoin(_root_url, download_link)
                package_name = download_link.split('/')[3]  #apk包名
                detail_data = requests.get(detail_link, headers=self.header).text
                soup = BeautifulSoup(detail_data, "html.parser")
                download = soup.find(id="download_link")["href"]
                if download not in res_parser.values():
                    res_parser[package_name] = download
                    count = count - 1
                if count == 0:
                    break
            if count > 0:
                page_num = page_num+1
        return res_parser


    def craw_apks(self,count=10, path="..\\apk\\"):
        data = PhoneUtil.getTodayData(self)
        apk_address = path+'APKPureTop'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        res_dic = self.parser_apks(count)
        for apk in res_dic.keys():
            self.logger.info("正在下载应用: "+apk)
            urllib.request.urlretrieve(res_dic[apk], apk_address+apk+".apk")

if __name__=="__main__":
    ApkPure = ApkPure()
    ApkPure.craw_apks(count=5)