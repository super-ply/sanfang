import logging
import requests
import re
import urllib
from urllib.request import urlopen
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

url = "https://apkcombo.com/zh-us/category/app/top-popular/?page="
class apkcombo_by:
    def get_url(self, num):
        apk_links = []
        whole_links = []
        page = int(num/42) + 1
        for i in range(page):
            download_url = url + str(i+1)
            headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
            wbdata = requests.get(download_url, headers=headers).text  # 网页内容
            soup = BeautifulSoup(wbdata, "html.parser")
            links = soup.find_all('a', attrs={"class": "gapp"})  # 获取当前页所有apk下载链接
            links = re.findall(r'href=(.*?)style', str(links))
            for link in links:
                link = eval(link)
                apk_link = "https://apkcombo.com" + link
                second_wbdata = requests.get(apk_link, headers=headers).text  # 网页内容
                soup = BeautifulSoup(second_wbdata, "html.parser")
                second_link = soup.find_all('a', attrs={"class": "abutton is-success is-fullwidth"})
                second_link = re.findall(r'href=(.*?)rel', str(second_link))
                if len(second_link) > 0:
                    second_link = second_link[0]
                    second_link = eval(second_link)
                else:
                    break
                third_link = "https://apkcombo.com" + second_link
                third_data = requests.get(third_link, headers=headers).text  # 网页内容
                soup = BeautifulSoup(third_data, "html.parser")
                third_link = soup.find_all('a', attrs={"class": "app"})  # 获取当前页所有apk下载链接
                third_link = re.findall(r'href=(.*?)rel=', str(third_link))
                if len(third_link) > 0:
                    third_link = third_link[0]
                    third_link = eval(third_link)
                    third_link = re.sub('amp;', '', third_link)
                    whole_links.append(third_link)
                else:
                    pass
            apk_links = whole_links[:num]
            print(apk_links)
        return apk_links

    def download_apk(self, num):
        date = PhoneUtil.getTodayData()
        save_path = "..\\apk\\"
        apk_address = save_path + 'ApkcomboBy' + date + "\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        download_apks = self.get_url(num)
        for apk in download_apks:
            if ".zip" in apk:
                apk_name = re.findall(r"name=(.*?).zip", apk)
            elif ".apk" in apk:
                apk_name = re.findall(r"name=(.*?).apk", apk)
            else:
                apk_name = ["null"]
            apk_name = apk_name[0]
            apk_name = "com" + str(apk_name) + "apk"
            for i in range(5):
                try:
                    print("正在下载:" + apk_name)
                    urllib.request.urlretrieve(apk, apk_address + apk_name)
                    print("下载完成")
                    logging.info("下载完成")
                    break
                except Exception as e:
                    print("fail:" + str(e))
                    print("网络问题，重新下载")






if __name__ == "__main__":
    a = apkcombo_by()
    #a.download_apk(4)

