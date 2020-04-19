import logging
from urllib.request import urlopen
import requests
import re
import urllib
from utils.utils import PhoneUtil
from bs4 import BeautifulSoup

url = "https://appstore.huawei.com/more/all"
class huaweiby:
    def get_url(self, num):
        apk_links = []
        whole_links = []
        page = int(num/24) + 1
        for i in range(page):
            download_url = url + "/"+str(i+1)
            headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
            wbdata = requests.get(download_url, headers=headers).text  # 网页内容
            soup = BeautifulSoup(wbdata, "html.parser")
            links = soup.find_all('a', attrs={"class": "btn-blue down"})  # 获取当前页所有apk下载链接
            links = re.findall(r'https(.*?)HWSW', str(links))
            apk_links = apk_links + links
            for link in apk_links:
                link = "https" + link + "HWSW"
                whole_links.append(str(link))
        return whole_links

    def download_apk(self, num):
        date = PhoneUtil.getTodayData(self)
        save_path = "..\\apk\\"
        apk_address = save_path + 'HuaweiByName' + date + "\\"
        PhoneUtil.checkAndCreatFolder(self, apk_address)
        all_apks = self.get_url(num)
        download_apks = all_apks[0:num]
        for apk in download_apks:
            apk_name = re.findall(r"/com(.*?)apk", apk)
            apk_name = apk_name[0]
            apk_name = "com" + str(apk_name) + "apk"
            for i in range(5):
                try:
                    print("正在下载:" + apk_name)
                    urllib.request.urlretrieve(apk, apk_address +apk_name)
                    print("下载完成")
                    logging.info("下载完成")
                    break
                except Exception as e:
                    print("fail:" + str(e))
                    print("重新下载")






if __name__ == "__main__":
    a = huaweiby()
    a.download_apk(2)

