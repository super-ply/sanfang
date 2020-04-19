# -*- coding:utf-8 -*-
import xlwt
from apk_tester import ApkManager


if __name__ == "__main__":
	a=ApkManager()
	result_lists = a.run()
	result = xlwt.Workbook() #创建一个Excel
	sheet1 = result.add_sheet('result') 
	sheet1.write(0,0,'序号') 
	sheet1.write(0,1,'手机序列号') 
	sheet1.write(0,2,'apk名称') 
	sheet1.write(0,3,'安装结果') 
	sheet1.write(0,4,'卸载结果')
	sheet1.write(0,5,'短MONKEY结果')
	sheet1.write(0,6,'MONKEYFAIL次数')
	sheet1.write(0,7,'MONKEYFAIL原因')
	line = 1
	for i in range(len(result_lists)):
		sheet1.write(i+1,0,str(i+1))
		sheet1.write(i+1,1,result_lists[i].sn)
		sheet1.write(i+1,2,result_lists[i].app_name)
		sheet1.write(i+1,3,result_lists[i].install_result)
		sheet1.write(i+1,4,result_lists[i].uninstall_result)
		sheet1.write(i+1,5,result_lists[i].monkey_result)
		sheet1.write(i+1,6,result_lists[i].fail_time)
		sheet1.write(i+1,7,result_lists[i].fail_reason)
	result.save('result.xls')