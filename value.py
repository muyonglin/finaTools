###################
#calculate daily value for holdings
##############
import sys
import pandas as pd
#sys.path.append("D:/programe-data/python_functions/")
sys.path.append("D:/codes/stocks/infomationTools")
from stockRelatedFunctions import queryValue

#holding stocks
#ETF and LOF should be sz/sh, not jj
holdings = {
	'港股':[
		['恒生ETF','159920','sz',1700],
		['H股ETF','510900','sh',4100]
		],
	'货币基金':[
		['银华日利','511880','sh',100],
		['华宝添益','511990','sh',105]
		],
	'美股欧股':[
		['德国30','000614','jj',300.24]
		],
	'A股':[
		['申万环保','163114','jj',16],
		['中证环保','001064','jj',3831.27+893.38],
		['广发医药','159938','sz',1300],
		['广发医药ETF','001180','jj',4816.48],
		['广发养老','000968','jj',3611.44],
		['中证红利','100032','jj',2514.78+2126.09],
		['建信中证500','000478','jj',2904.61],
		['沪深300','000961','jj',1],
		['50ETF','510050','sh',200],
		['工商银行','601398','sh',100,'stock'],
		['创业板ETF','110026','jj',318.17],
		['广发创业','003765','jj',625.79],
		['500ETF','510500','sh',300],
		['券商ETF','512000','sh',1600],
		['环保ETF','512580','sh',1100],
		['银行ETF','512800','sh',400],
		['中证传媒','004752','jj',1203.49+641.35],
		['传媒ETF','512980','sh',400],
		['1000ETF','512100','sh',200],
		['富国沪深300增强','100038','jj',332.56]
		],
	'分级A':[
		['环保A','150184','sz',100]
		],
	'分级B':[
		['环保B','150185','sz',100]
		],
	'黄金白银':[
		['黄金ETF','518880','sh',200]
		,['建行纸白银','paperSilver','ccb',594,'silver']
		],
	'债券':[
		['广发纯债债券A','270048','jj',1023.08],
		['博时信用纯债','050027','jj',1035.78],
		['广发中债','003376','jj',3184.61],
		['华夏海外收益债A','001061','jj',1978.66],
		['兴全可转债混合','340001','jj',578.29]
		],
	'石油':[
		['石油基金','160416','sz',400],
		['华宝油气','162411','sz',1395+697+0.9]
		]
}


dividen = 74371.22913
cash = [
	['蚂蚁聚宝',0],
	['盈米宝',0],
	['工薪宝',1040.71],
	['建行存款',631.13],
	['华宝证券现金',2300.14+10104.21+1536.15]
	]

cashAmount = pd.DataFrame(cash).iloc[:,1].sum()

keySeq = ['港股','货币基金','美股欧股','A股','分级A','分级B','黄金白银','债券','石油']
valueTable = []
for key in keySeq:
	for item in holdings[key]:
		value = queryValue(item)
		if value != -1:
			valueTable.append([item[0],value * item[3],value,item[3]])
		else:
			print("values wrong!")
			break	
valueTable.append(['现金',cashAmount,0,0])
wholeAmount = pd.DataFrame(valueTable).iloc[:,1].sum()
valueTable.append(['总额',wholeAmount,0,0])	
valueTable.append(['份数',dividen,0,0])
valueTable.append(['净值',wholeAmount/dividen,0,0])	

df = pd.DataFrame(valueTable)

import datetime
df.to_csv("D:/Desktop/"+str(datetime.date.today())+".txt",encoding='utf-8'
	,index=False,header=False)
#for item in valueTable:
#	print("%s\t%f\t%f\t%f\n"%(item[0],item[1],item[2],item[3]))

