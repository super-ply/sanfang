#coding=utf-8
import os
import datetime

class MyUtil:
	def checkAndCreatFolder(self,folder_name):
		if os.path.exists(folder_name):
			pass
		else:
			os.makedirs(folder_name)

	def getTodayData(self):
		data = str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(".","_").replace(":","_")
		return data

	def getFiles(self,path=os.getcwd(), file_type='txt'):
		need_files=[] 
		for root, dirs, files in os.walk(path): 
			for file in files: 
				if os.path.splitext(file)[1] == '.'+file_type:
					need_files.append(os.path.join(root, file))
		return need_files


if __name__=='__main__':
	MyUtil=MyUtil()
	MyUtil.getFiles(file_type='py')