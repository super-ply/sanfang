# -*- coding:utf-8 -*-
import os,time
import logging
import xlwt
import threading
from my_utils import MyUtil
from devices import Devices

class ApkManager:
	'''
	初始化，增加log信息，增加机器检测
	'''
	devices = ['5389beb8']
	#devices = ['HQ698V3682', 'HQ68CA0041']
	def __init__(self, devices=devices):
		self.until = MyUtil()
		self.until.checkAndCreatFolder("log")
		self.until.checkAndCreatFolder("monkeyresult")
		self.app_lists = self.until.getFiles(file_type='apk')
		logging.basicConfig(
			level=logging.DEBUG,
			format='%(asctime)s %(levelname)s %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S',
			filename='log//runtime.log',
			filemode='a+'
		)
		if len(devices) == 0:
			raise AssertionError('No devices online')
		else:
			self.devices=devices


		
	def monkey(self,device,appname):
		'''
		执行monkey
		@device  设备序列号
		@应用包名
		'''
		os.system("adb -s " + device + " shell monkey -p " + appname.strip(".apk") + " --ignore-crashes --ignore-timeouts --monitor-native-crashes --throttle 1000 --ignore-native-crashes -s 500 -v -v -v 50 >>monkeyresult/"+device+appname+"monkey.txt")
		monkey_result = self.analyseMonkeylog(device, appname)
		return monkey_result

	def analyseMonkeylog(self, device, appname):
		'''
		分析monkeylog
		@device  设备序列号
		@应用包名
		'''
		monkey_result = "pass"
		monkey_status = "null"
		monkeylog = open("monkeyresult//"+device+appname+"monkey.txt",'r')
		line = monkeylog.readline()
		fail_times = 0
		fail_reson = ''
		while line:
			#FATAL 读取两行
			if "Exception" in line:
				monkey_result = "fail"
				fail_times = fail_times + 1
				fail_reson = fail_reson + str(line)
			if 'Monkey finished' in line:
				monkey_status = "done"
			line = monkeylog.readline()
		monkeylog.close()
		if monkey_result == "pass" and monkey_status == "done" :
			monkey_result = "pass"
		else:
			monkey_result = "fail"
		if monkey_status != "done":
			fail_reson = fail_reson + "Not begin monkey test, please check apk if install success."

		return [monkey_result, str(fail_times), fail_reson]

	def uninstall(self, device, appname):
		'''
		卸载apk
		@device 设备序列号
		@appname  包名   这里不需要路径 因为卸载只需要包名
		'''
		with os.popen('adb -s ' + device +' uninstall '+appname.strip(".apk"), 'r') as un:
			untext = un.read()
			if 'Success' not in untext:
				uninstall_result = "fail"
			else:
				uninstall_result = "pass"
		un.close()
		return uninstall_result

	def install(self, device, appname):
		'''
		安装apk
		@device 设备序列号
		@appname apk路径
		'''
		with os.popen('adb -s ' + device +' install '+appname, 'r') as ins:
			intext = ins.read()
			if 'Success' not in intext:
				install_result = "fail"
			else:
				install_result = "pass"
		ins.close()
		return install_result

		
	def singleDueTest(self,device):		
			#单机测试方法
		test_results=[]
		for app in self.app_lists:
				appname = app.split("\\")[-1]
				logging.debug(device+"****"+appname+"  begin test")
				install_result = self.install(device,app)
				monkey_results = self.monkey(device,appname)
				monkey_result = monkey_results[0]
				fail_time = monkey_results[1]
				fail_reson = monkey_results[2]
				uninstall_result = self.uninstall(device,appname.strip(".apk"))
				logging.debug(device+"****"+appname+"  end test")
				test_info=Devices(device,appname,install_result,uninstall_result,monkey_result,fail_time,fail_reson)
				test_results.append(test_info)
		return test_results
	
	def run(self,devices=devices):
		'''
		运行
		@devices 机器列表
		'''
		#检测apk是否存在
		
		if len(self.app_lists) == 0:
			raise AssertionError('No apk folder or no .apk')

		##############################################################################
		#单机器处理
		if len(devices)==1:
			test_results=self.singleDueTest(devices[0])
			return test_results
		##############################################################################
		#多机器处理
		else:
			test_results = []
			for device in devices:
				locals()[device]=MyThread(device)
			for device in devices:
				locals()[device].start()
			for device in devices:
				locals()[device].join()
			for device in devices:
				test_results = test_results+locals()[device].get_result()

			'''
			for device in devices:
				locals()[device] = threading.Thread(target=singleDueTest,args=(device,))
			for device in devices:
				locals()[device].start()
			for device in devices:
				locals()[device].join()
				print('**********')
				print(locals()[device].get_result)
			'''
		
			return test_results
			pass



class MyThread(threading.Thread):
	"""docstring for judge_video"""
	def __init__(self, arg):
		self.apkmanager = ApkManager()
		super(MyThread, self).__init__()
		self.arg = arg
 
	def run(self):
		self.result=self.apkmanager.singleDueTest(self.arg)
 
	def get_result(self):
		return self.result

if __name__ == "__main__":
	a=ApkManager()
	#device = ['5389beb8']
	#a.install(device,appname)
	a.run()
	#a.wb.save('fuck.xls')
	pass
