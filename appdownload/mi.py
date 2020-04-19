#coding=utf-8
import logging
import requests
import sys
import re
import urllib
from bs4 import BeautifulSoup
sys.path.append("..")
from utils.utils import PhoneUtil


class MiDownload:

    def __init__(self):
        logging.basicConfig(filename='..\\log\\runtime.log', level=logging.INFO)
        self.logger = logging.getLogger('MITOP'+PhoneUtil.getTodayData(self))

    def parser_apks(self,count=10):
        '''小米应用市场'''
        _root_url="http://app.mi.com"
        res_parser={}
        page_num=1
        while count:
            wbdata = requests.get("http://app.mi.com/topList?page="+str(page_num)).text
            soup=BeautifulSoup(wbdata,"html.parser")
            links=soup.find_all('h5')
            for link in links:
                if "/details?" in str(link):
                    link=(str(link).split('"'))[1]
                    detail_link=urllib.parse.urljoin(_root_url, link)
                    package_name=detail_link.split("=")[1]
                    download_page=requests.get(detail_link).text
                    soup1=BeautifulSoup(download_page,"html.parser")
                    try:
                        download_link=soup1.find(class_="download")["href"]
                        download_url=urllib.parse.urljoin(_root_url, str(download_link))
                    except:
                        self.logger.info("异常app网页"+str(package_name))
                    if download_url not in res_parser.values():
                        res_parser[package_name]=download_url
                        count=count-1
                    if count==0:
                        break
            if count >0:
                page_num=page_num+1
        return res_parser


    def craw_apks(self,count=10, path="..\\apk\\"):
        data=PhoneUtil.getTodayData(self)
        apk_address=path+'MiTop'+data+"\\"
        PhoneUtil.checkAndCreatFolder(self,apk_address)
        res_dic=self.parser_apks(count)
        self.logger.info("爬取apk数量为: "+str(len(res_dic)))
        for apk in res_dic.keys():
            self.logger.info("正在下载应用: "+apk)
            urllib.request.urlretrieve(res_dic[apk],apk_address+apk+".apk")
if __name__=="__main__":
    MiBy=MiDownload()
    MiBy.craw_apks(10)