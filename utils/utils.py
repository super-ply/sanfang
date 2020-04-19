#coding=utf-8
import os
import datetime

"""
工具类
设备序列号获取  
品牌获取
"""


class PhoneUtil:
	def checkAndCreatFolder(self,foldername):
		if os.path.exists(foldername):
			pass
		else:
			os.makedirs(foldername)

	def getTodayData(self):
		data = str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(".","_").replace(":","_")
		return data
if __name__=='__main__':
	PhoneUtil=PhoneUtil()
	PhoneUtil.getTodayData()