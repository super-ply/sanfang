# -*- coding:utf-8 -*-
import logging

class Devices:
	def __init__(self,sn='null',app_name='null',install_result='null',uninstall_result='null',monkey_result='null',fail_time='0',fail_reason='null'):
		logging.basicConfig(
			level = logging.INFO,
			format = '%(asctime)s %(levelname)s %(message)s',
			datefmt = '%a, %d %b %Y %H:%M:%S',
			filename = 'log//runtime.log',
			filemode = 'a+'
		)
		self.sn = sn
		self.app_name = app_name
		self.install_result = install_result
		self.uninstall_result = uninstall_result
		self.monkey_result = monkey_result
		self.fail_time = fail_time
		self.fail_reason = fail_reason
		logging.info("**"+self.sn+"**"+self.app_name+"**"+self.install_result+"**"+self.uninstall_result+"**"+self.monkey_result+"**"+self.fail_time+"**"+self.fail_reason+"**")
if __name__ == "__main__":
	#a=Devices("testA",'taobao')
	pass
