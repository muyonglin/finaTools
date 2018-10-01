# class backTest(generalFunction):
# 	"""docstring for backTest"""
# 	def __init__(self, stockCode,startDate='2000-1-1'
# 		, calDatabase='D:/programe-data/database/stockHistInfoDatabase/calInfo.db'):
# 		super(backTest, self).__init__()
# 		self.sc = stockCode
# 		self.dc = calDatabase
# 		self.sad = startDate

# 	def getPBGXLData(self):
# 		tableName = "HistCal_" + self.sc
# 		try:
# 			PB_GXL = generalFunction.fetchDataFromDatabase(self,self.dc,tableName,['date','PB','guxilv'])
# 			#PB_GXL, from oldest to today
# 			PB_GXL.sort(key=lambda tup: tup[0])
# 		except Exception as e:
# 			print('Hist PB_GXL ' + self.sc + str(e))
# 			PB_GXL = 0
# 		return(PB_GXL)	

# 	def dateSeries(self):
# 		import datetime as dt
# 		end = dt.datetime.strptime(self.sod,'%Y-%m-%d')
# 		start = dt.datetime.strptime(self.sad,'%Y-%m-%d')
		
# 		td = dt.timedelta(days=1)	
# 		dtList = []
# 		while start < end:
# 			start += td
# 			if start.weekday() == 6:
# 				dtList.append(start)
# 		return(dtList)		

# 	def getNearestDate(self,dateList,targetDate):
# 		import datetime as dt
# 		#print(targetDate)
# 		for i in range(0,(len(dateList)-1)):
# 			if targetDate >= dateList[i] and targetDate < dateList[i+1]:
# 				return(dateList[i])
# 	def selectStocks(self,histDataDF):
# 		#begin test only when stocks has more than 3 years of data
# 		if len(histDataDF) < 840:
# 			return(False)
# 		elif (histDataDF.iloc[:,2] == 0).sum()/len(histDataDF.iloc[:,2]) > 0.1:	
# 			return(False)
# 		else:
# 			#GXL higher than 90% and > 3%, PB lower than 90%
# 			#print(histDataDF.iloc[:,2].quantile(0.9))
# 			if histDataDF.iloc[-1,2] > histDataDF.iloc[:,2].quantile(0.9) and histDataDF.iloc[-1,2] > 0.03 and histDataDF.iloc[-1,1] < histDataDF.iloc[:,1].quantile(0.1):
# 				return(True)
# 			else:
# 				return(False)
								

# 	def testForOneStock(self,resultDict={}):
# 		PB_GXL = self.getPBGXLData()
# 		if PB_GXL == 0:
# 			return(resultDict)
# 		#data time longer than 3 years	
# 		elif len(PB_GXL) > 840:
# 			#print(resultDict)
# 			import pandas as pd
# 			import datetime as dt
# 			dateList = [dt.datetime.strptime(i[0],"%Y-%m-%d") for i in PB_GXL]
# 			#print(dateList)
# 			self.sod = PB_GXL[-1][0]		
# 			dateRange = self.dateSeries()
# 			PB_GXL_df = pd.DataFrame(PB_GXL)
# 			#PB_GXL_df.iloc[:,0] = pd.to_datetime(PB_GXL_df.iloc[:,0])
# 			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
# 			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 
# 			for item in dateRange:
# 				if item > dateList[0]:					
# 					#print(item)
# 					endDate = self.getNearestDate(dateList,item)
# 					#print(endDate)
# 					dateIndex = dateList.index(endDate)
# 					dataForTest = PB_GXL_df.iloc[0:dateIndex,:]
# 					if self.selectStocks(dataForTest):
# 						if item in resultDict.keys():
# 							resultDict[item].append(self.sc)
# 						else:
# 							resultDict[item] = [self.sc]
# 			return(resultDict)
# 		else:
# 			return(resultDict)

# 	def onlyTestLatestTime(self):
# 		PB_GXL = self.getPBGXLData()
# 		if PB_GXL == 0:
# 			return(0)
# 		else:	
# 			import pandas as pd
# 			PB_GXL_df = pd.DataFrame(PB_GXL)
# 			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
# 			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 			
# 			#print(PB_GXL_df)	
# 			if self.selectStocks(PB_GXL_df):
# 				return(self.sc)
# 			else:
# 				return(0)	

# 	def selectStockForSell(self,histDataDF):
# 		#bought stock already saturate all the requirment
# 		#sell when PB is higher than 70% times
# 		if histDataDF.iloc[-1,1] > histDataDF.iloc[:,1].quantile(0.7):
# 			return(True)
# 		else:
# 			return(False)
				
# 	def testForSell(self,resultDict={}):
# 		PB_GXL = self.getPBGXLData()
# 		if PB_GXL == 0:
# 			return(0)
# 		else:
# 			import pandas as pd
# 			import datetime as dt
# 			dateList = [dt.datetime.strptime(i[0],"%Y-%m-%d") for i in PB_GXL]
# 			#print(dateList)
# 			self.sod = PB_GXL[-1][0]		
# 			dateRange = self.dateSeries()
# 			PB_GXL_df = pd.DataFrame(PB_GXL)
# 			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
# 			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 

# 			for item in dateRange:
# 				if item > dateList[0]:					
# 					#print(item)
# 					endDate = self.getNearestDate(dateList,item)
# 					#print(endDate)
# 					dateIndex = dateList.index(endDate)
# 					dataForTest = PB_GXL_df.iloc[0:dateIndex,:]
# 					if self.selectStockForSell(dataForTest):
# 						if item in resultDict.keys():
# 							resultDict[item].append(self.sc)
# 						else:
# 							resultDict[item] = [self.sc]
# 			return(resultDict)
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
		
class sinaFinanParser(generalFunction):
	"""docstring for sinaFinanParser"""
	def __init__(self, stockCode, stockExchange="sh"):
		import datetime
		self.sc = stockCode
		self.todayYear = str(datetime.datetime.today())[0:4]
		self.htmlForYearRange = self.getNewestPage()
		self.yearList = self.yearRange()
		self.urlList = self.constructUrlList()
		self.finanStrList = self.htmlListFordata()
		#self.dateList = self.getBaoGaoRiQi()
		#self.meiGuShouYiList = self.getTanBoMeiGuShouYi()
		#self.meiGuJingZiChan = self.getTiaoZhengMeiGuJingZiChan()

	def getNewestPage(self):
		#http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/600151/displaytype/4.phtml
		url = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/" + self.sc + "/ctrl/" + self.todayYear + "/displaytype/4.phtml"
		html = generalFunction.tryUrl(self,url,10,"gb2312")
		return(html)
	#get all matched result in re
	def yearRange(self):
		import re
		#yearList = re.findall("<table width.*历年数据:.*?(>\d\d\d\d<).*?/table",self.htmlForYearRange)
		#tmpList = re.findall("<table width.*历年数据.*?/table>",self.htmlForYearRange)
		tmpList = re.findall("<table width.*\r\n.*\r\n.*历年数据.*\r\n.*\r\n.*\r\n.*/table>",self.htmlForYearRange)
		#with open("test.txt",'w',encoding="utf-8") as f:
		#	f.write(self.htmlForYearRange)
		#print(tmpList)
		#print(self.htmlForYearRange)
		yearList = re.findall(">(\d\d\d\d)<",tmpList[0])
		return(yearList)
	def constructUrlList(self):
		urlList = []
		for item in self.yearList:
			url = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/" + self.sc + "/ctrl/" + item + "/displaytype/4.phtml"
			urlList.append(url)
		#print(urlList)	
		return(urlList)	
	def htmlListFordata(self):
		import re
		finanStrList = []
		#htmlList = []
		for item in self.urlList:
			html = generalFunction.tryUrl(self,item,10,'gb2312')
			#htmlList.append(html)
			finanStrTmp = re.findall("财务指标</th>.*\r\n.*\r\n.*\r\n.*\r\n.*\r\n.*/table>",html)
			finanStrList.append(finanStrTmp)
		return(finanStrList)
	# def getBaoGaoRiQi(self):
	# 	import re
	# 	dateList = []
	# 	for item in self.finanStrList:			
	# 		tmpDateList = re.findall(">(\d\d\d\d-\d\d-\d\d)<",item[0])
	# 		dateList.append(tmpDateList)
	# 	return(dateList)			
	def getTanBoMeiGuShouYi(self):
		import re, datetime
		meiGuShouYiList_1 = []
		for item in self.finanStrList:
			tmpDateList = re.findall(">(\d\d\d\d-\d\d-\d\d)<",item[0])
			tmpMeiGuYingLi_1 = re.findall("摊薄每股收益.*?加权每股收益",item[0])
			#tmpMeiGuYingLi_2 = re.findall(">(\d\.\d+)<",tmpMeiGuYingLi_1[0])
			tmpMeiGuYingLi_2 = re.findall("<td>(.*?)</td>",tmpMeiGuYingLi_1[0])
			tmpList = [] #[(报告时间，累计摊薄每股收益，每季摊薄每股收益，年末/最新摊薄每股收益，滚动摊薄每股收益),(),(),()]
			if tmpDateList != []:
				#print(tmpMeiGuYingLi_2)	
				if len(tmpMeiGuYingLi_2) == 1 and tmpDateList[5:9] != '03-31':
					tmpList.append((tmpDateList[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],"--",tmpMeiGuYingLi_2[0]))
				else:
					for i in range(len(tmpDateList) - 1):
						if (i + 1)< len(tmpMeiGuYingLi_2) and tmpMeiGuYingLi_2[i] != '--' and tmpMeiGuYingLi_2[i+1] != '--' and (datetime.datetime.strptime(tmpDateList[i],"%Y-%m-%d") - datetime.datetime.strptime(tmpDateList[i+1],"%Y-%m-%d")) < datetime.timedelta(100):
							tmpList.append((tmpDateList[i],tmpMeiGuYingLi_2[i],str(round(float(tmpMeiGuYingLi_2[i]) - float(tmpMeiGuYingLi_2[i+1]),4)),tmpMeiGuYingLi_2[0]))
						else:
							tmpList.append((tmpDateList[i],tmpMeiGuYingLi_2[i],"--",tmpMeiGuYingLi_2[0]))

					tmpList.append((tmpDateList[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[0]))
				meiGuShouYiList_1.append(tmpList)
		meiGuShouYiList_2 = []
		for i in range(len(meiGuShouYiList_1)-1):
			for item in meiGuShouYiList_1[i]:
				meiGuShouYiList_2.append((item[0],item[1],item[2],meiGuShouYiList_1[i+1][0][-1]))	
		for item in meiGuShouYiList_1[len(meiGuShouYiList_1) - 1]:
			meiGuShouYiList_2.append((item[0],item[1],item[2],"--"))	
		meiGuShouYiList_3 = []
		for i in range(len(meiGuShouYiList_2)-4):
			if (datetime.datetime.strptime(meiGuShouYiList_2[i][0],"%Y-%m-%d") - datetime.datetime.strptime(meiGuShouYiList_2[i+3][0],"%Y-%m-%d")) > datetime.timedelta(270) and (datetime.datetime.strptime(meiGuShouYiList_2[i][0],"%Y-%m-%d") - datetime.datetime.strptime(meiGuShouYiList_2[i+3][0],"%Y-%m-%d")) < datetime.timedelta(280) and '--' not in [meiGuShouYiList_2[i][2],meiGuShouYiList_2[i+1][2],meiGuShouYiList_2[i+2][2],meiGuShouYiList_2[i+3][2]]:
				meiGuShouYiList_3.append((meiGuShouYiList_2[i][0],meiGuShouYiList_2[i][1],meiGuShouYiList_2[i][2],meiGuShouYiList_2[i][3],str(round(float(meiGuShouYiList_2[i][2]) + float(meiGuShouYiList_2[i+1][2]) + float(meiGuShouYiList_2[i+2][2]) + float(meiGuShouYiList_2[i+3][2]),4))))
			else:
				meiGuShouYiList_3.append((meiGuShouYiList_2[i][0],meiGuShouYiList_2[i][1],meiGuShouYiList_2[i][2],meiGuShouYiList_2[i][3],'--'))
		return(meiGuShouYiList_3)	
	def getTiaoZhengMeiGuJingZiChan(self):
		import re
		meiGuJingZiChanList_1 = []
		for item in self.finanStrList:
			tmpDateList = re.findall(">(\d\d\d\d-\d\d-\d\d)<",item[0])
			tmpMeiGuJingZiChan_1 = re.findall("每股净资产_调整后.*?每股经营性现金流",item[0])
			tmpMeiGuJingZiChan_2 = re.findall("<td>(.*?)</td>",tmpMeiGuJingZiChan_1[0])
			if tmpDateList != []:
				for i in range(len(tmpDateList)):
					meiGuJingZiChanList_1.append((tmpDateList[i],tmpMeiGuJingZiChan_2[i]))
		#[(报告时间，每股净资产),(),(),()]
		return(meiGuJingZiChanList_1) 
	
	def getRecentTanBoMeiGuShouYi(self):
		#recent financial data URL
		#http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/603779/displaytype/4.phtml
		import re, datetime
		urlList = []
		if len(self.yearList) < 3:
			RcentMgsy = self.getTanBoMeiGuShouYi()
			return(RcentMgsy)
		else:				
			for i in range(3):
				url = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/" + self.sc + "/ctrl/" + self.yearList[i] + "/displaytype/4.phtml"
				#print(url)
				urlList.append(url)
			finanStrList = []
			for item in urlList:
				html = generalFunction.tryUrl(self,item,10,'gb2312')
				#htmlList.append(html)
				finanStrTmp = re.findall("财务指标</th>.*\r\n.*\r\n.*\r\n.*\r\n.*\r\n.*/table>",html)
				finanStrList.append(finanStrTmp)
			
			meiGuShouYiList_1 = []
			for item in finanStrList:
				tmpDateList = re.findall(">(\d\d\d\d-\d\d-\d\d)<",item[0])
				tmpMeiGuYingLi_1 = re.findall("摊薄每股收益.*?加权每股收益",item[0])
				#tmpMeiGuYingLi_2 = re.findall(">(\d\.\d+)<",tmpMeiGuYingLi_1[0])
				tmpMeiGuYingLi_2 = re.findall("<td>(.*?)</td>",tmpMeiGuYingLi_1[0])
				tmpList = [] #[(报告时间，累计摊薄每股收益，每季摊薄每股收益，年末/最新摊薄每股收益，滚动摊薄每股收益),(),(),()]
				if tmpDateList != []:
					#print(tmpMeiGuYingLi_2)	
					if len(tmpMeiGuYingLi_2) == 1 and tmpDateList[5:9] != '03-31':
						tmpList.append((tmpDateList[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],"--",tmpMeiGuYingLi_2[0]))
					else:
						for i in range(len(tmpDateList) - 1):
							if (i + 1)< len(tmpMeiGuYingLi_2) and tmpMeiGuYingLi_2[i] != '--' and tmpMeiGuYingLi_2[i+1] != '--' and (datetime.datetime.strptime(tmpDateList[i],"%Y-%m-%d") - datetime.datetime.strptime(tmpDateList[i+1],"%Y-%m-%d")) < datetime.timedelta(100):
								tmpList.append((tmpDateList[i],tmpMeiGuYingLi_2[i],str(round(float(tmpMeiGuYingLi_2[i]) - float(tmpMeiGuYingLi_2[i+1]),4)),tmpMeiGuYingLi_2[0]))
							else:
								tmpList.append((tmpDateList[i],tmpMeiGuYingLi_2[i],"--",tmpMeiGuYingLi_2[0]))

						tmpList.append((tmpDateList[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[len(tmpMeiGuYingLi_2)-1],tmpMeiGuYingLi_2[0]))
					meiGuShouYiList_1.append(tmpList)
			meiGuShouYiList_2 = []
			for i in range(len(meiGuShouYiList_1)-1):
				for item in meiGuShouYiList_1[i]:
					meiGuShouYiList_2.append((item[0],item[1],item[2],meiGuShouYiList_1[i+1][0][-1]))	
			for item in meiGuShouYiList_1[len(meiGuShouYiList_1) - 1]:
				meiGuShouYiList_2.append((item[0],item[1],item[2],"--"))	
			meiGuShouYiList_3 = []
			for i in range(len(meiGuShouYiList_2)-4):
				if (datetime.datetime.strptime(meiGuShouYiList_2[i][0],"%Y-%m-%d") - datetime.datetime.strptime(meiGuShouYiList_2[i+3][0],"%Y-%m-%d")) > datetime.timedelta(270) and (datetime.datetime.strptime(meiGuShouYiList_2[i][0],"%Y-%m-%d") - datetime.datetime.strptime(meiGuShouYiList_2[i+3][0],"%Y-%m-%d")) < datetime.timedelta(280) and '--' not in [meiGuShouYiList_2[i][2],meiGuShouYiList_2[i+1][2],meiGuShouYiList_2[i+2][2],meiGuShouYiList_2[i+3][2]]:
					meiGuShouYiList_3.append((meiGuShouYiList_2[i][0],meiGuShouYiList_2[i][1],meiGuShouYiList_2[i][2],meiGuShouYiList_2[i][3],str(round(float(meiGuShouYiList_2[i][2]) + float(meiGuShouYiList_2[i+1][2]) + float(meiGuShouYiList_2[i+2][2]) + float(meiGuShouYiList_2[i+3][2]),4))))
				else:
					meiGuShouYiList_3.append((meiGuShouYiList_2[i][0],meiGuShouYiList_2[i][1],meiGuShouYiList_2[i][2],meiGuShouYiList_2[i][3],'--'))
		return(meiGuShouYiList_3)
		
	def getRecentTiaoZhengMeiGuJingZiChan(self):
		#recent financial data URL
		#http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/603779/displaytype/4.phtml
		import re
		url = "http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/" + self.sc + "/displaytype/4.phtml"
		html = generalFunction.tryUrl(self,url,10,'gb2312')
		tmpDateList = re.findall(">(\d\d\d\d-\d\d-\d\d)<",html)
		tmpMeiGuJingZiChan_1 = re.findall("每股净资产_调整后.*?每股经营性现金流",html)
		tmpMeiGuJingZiChan_2 = re.findall("<td>(.*?)</td>",tmpMeiGuJingZiChan_1[0])
		tmpList = []
		for i in range(len(tmpMeiGuJingZiChan_2)):
			tmpList.append((tmpDateList[i],tmpMeiGuJingZiChan_2[i]))
		return(tmpList)	

	#get fenhong peisong data from sina	
	def getFenHongPeiSong(self):
		import re
		#http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600137.phtml
		url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/' + self.sc + '.phtml'
		html = generalFunction.tryUrl(self,url,10,'gb2312')
		#re.DOTALL makes . matches any character
		tmpStr = re.findall("<!--分红 begin-->(.*?)<!--分红 end-->",html,re.DOTALL)
		tmpFenHong_1 = re.findall("<tbody>(.*?)</tbody>",tmpStr[0],re.DOTALL)
		tmpFenHong_2 = re.findall("<tr>(.*?)</tr>",tmpFenHong_1[0],re.DOTALL)
		#print(tmpFenHong_2)
		tmpFenHong_3 = []
		for i in range(len(tmpFenHong_2)):
			tmp = re.findall("<td>(.*?)</td>",tmpFenHong_2[i])
			if tmp[5] == '--'  and i == 0:
				continue
			elif tmp[5] == '--'  and i != 0:
				tmpFenHong_3.append((tmp[0],{'送':tmp[1],'转':tmp[2],'派':tmp[3]}))
			else:
				tmpFenHong_3.append((tmp[5],{'送':tmp[1],'转':tmp[2],'派':tmp[3]}))
		#[(date,{'送':0,'转':0,'派':0}),(),()]
		return(tmpFenHong_3)	
			
					
#parser for yahoo price historical data
#yahoo url 
#	http://table.finance.yahoo.com/table.csv?s=000001.sz
#	http://table.finance.yahoo.com/table.csv?s=600000.ss
#http://basic.10jqka.com.cn/601398/finance.html

class yahooPriceParser(generalFunction):
	"""docstring for priceParser
	   @input: stock code, stock exchange, 
	   		   startDate ('yyyy-mm-dd'), stopDate ('yyyy-mm-dd') 

	   @methods: use yahoo finance as price data source
	   @output:		   
	"""
	def __init__(self, stockCode, stockExchange='.SS', startDate = 'N', stopDate = 'N', dataSource='yh'):
		self.sc = stockCode
		self.se = stockExchange
		self.ds = dataSource
		self.startDate = startDate
		self.stopDate = stopDate

		#print(self.url)
		#self.html = tryUrl(self.url)
		self.jsonData = self.extractHistPrice()
	def getTime(self):
		if self.startDate == 'N' and self.stopDate == 'N':
			self.getFirstAndLastTradDate()
		else:
			import datetime
			self.startStamp = str(int(datetime.datetime.strptime(self.startDate,'%Y-%m-%d').timestamp()))
			self.stopStamp = str(int(datetime.datetime.strptime(self.stopDate,'%Y-%m-%d').timestamp()))			

	def constructURL(self):
		if self.ds == 'yh':
			#print(self.sc,self.se,self.startStamp,self.stopStamp)
			self.url = 'https://finance.yahoo.com/quote/' + self.sc + self.se + '/history?period1=' + self.startStamp + '&period2=' + self.stopStamp + '&interval=1d&filter=history&frequency=1d'

		
	def extractHistPrice(self):
		import re
		self.getTime()
		self.constructURL()
		html = generalFunction.tryUrl(self,self.url,10)
		priceJson = re.findall('HistoricalPriceStore\":(.*?}]})',html)[0]
		return(priceJson)

	def parseJson(self):
		import json
		transDict = json.loads(self.jsonData)
		return(transDict)
			
	def getFirstAndLastTradDate(self):
		import datetime
		import re
		self.stopStamp = str(int(datetime.datetime.today().timestamp()))
		url1 = 'https://finance.yahoo.com/quote/'+ self.sc + self.se + '/history?interval=1d&filter=history&frequency=1d'
		html1 =generalFunction.tryUrl(self,url1,10)
		self.startStamp = re.findall("firstTradeDate\":(\d*)",html1)[0]	
		#print(self.startStamp)

	def getRecentPrice(self):
		import datetime
		import re, json
		self.stopStamp = str(int(datetime.datetime.today().timestamp()))
		url1 = 'https://finance.yahoo.com/quote/'+ self.sc + self.se + '/history?interval=1d&filter=history&frequency=1d'
		html1 =generalFunction.tryUrl(self,url1,10)
		priceJson = re.findall('HistoricalPriceStore\":(.*?}]})',html1)[0]
		transDict = json.loads(priceJson)['prices']
		return(transDict)	
							

class constructDatabase(generalFunction):
	"""docstring for constructDatabase
		@input: stock id
		@method: query yahoo for price data 
			query sina for financial data
	"""
	def __init__(self, stockCode, stockExchange='.SS', startDate = 'N', stopDate = 'N',databasePathDefault="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"):
		super(constructDatabase, self).__init__()
		self.sc = stockCode
		self.se = stockExchange
		self.dp = databasePathDefault
		self.startDate = startDate
		self.stopDate = stopDate
		#self.dpf = finaDatabase

		#self.getPriceAndPutIntoDatabase()
		#self.writeMeiGuJingZiChanToDatabase()
		#self.writeGunDongJingZhiMeiGuShouYiToDatabase()
	def getFianFromXueQiuAndWriteIntoDatabase(self,dataBasePath):
		import sqlite3
		#results in {'list':[{},{}]} format
		fina = xueQiuPriceParser(self.sc,self.se).downloadAllFinanDataFromXueQiu()
		if fina['list'] == None:
			print(fina)
		conn = sqlite3.connect(dataBasePath)
		cursor = conn.cursor()
		tableNameF = "HiistFinance_" + self.sc

		cursor.execute('''create table if not exists %s 
			(date text primary key, basiceps float
			,naps float, weightedroe float, netincgrowrate float
			,salegrossprofitrto float)''' %(tableNameF))
		for item in fina['list']:
			#print(item['reportdate'])
			dateIn = item['reportdate'][0:4] + "-" + item['reportdate'][4:6] + "-" + item['reportdate'][6:8]  
			cursor.execute('''insert or ignore into %s 
				(date, basiceps, naps, weightedroe, netincgrowrate, salegrossprofitrto) 
				values (?,?,?,?,?,?)''' %(tableNameF),
				(dateIn,item['basiceps'],item['naps'],item['weightedroe'],item['netincgrowrate'],item['salegrossprofitrto']))
		conn.commit()
		cursor.close()
		conn.close()	
	def getPriceFromTencentAndPutIntoDatabase(self):
		import sqlite3
		if self.se == '.SS':
			se = 'sh'
		elif self.se == '.SZ':
			se = 'sz'	
		price = tencentPriceParser(self.sc,se).getkLineData()
		#print(price[0:5])
		#分红日 data
		#["2017-07-11","5.000","5.060","5.080","4.970","2489282.000",{"nd":"2016","fh_sh":"2.343","djr":"2017-07-10","cqr":"2017-07-11","FHcontent":"10\u6d3e2.343\u5143"}]
		#每日 data
		#["2017-07-12","5.060","5.080","5.150","5.050","2198352.000"]
		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		tableNameH = "HistPrice_" + self.sc + "_tencent"
		tableNameD = "Dividend_" + self.sc + "_tencent"

		cursor.execute('''create table if not exists %s 
			(date text primary key,
			open text, close text, high text,
			 low text, volume text)'''%(tableNameH))
		cursor.execute('''create table if not exists %s
			(date text primary key, FHcontent text, cqr text,
			 djr text, fh_sh text,nd text)''' %(tableNameD))
		# on duplicate key update 报错 (sqllite has no on duplicate key update syntax)
		#on conflict == or is similar to on duplicate key
		#sqlite specific
		#http://www.sqlite.org/lang_conflict.html
		for item in price:
			if len(item) == 6:
				cursor.execute("""insert or ignore into %s (date, open, close, high, low, volume) values (?,?,?,?,?,?)"""
						% (tableNameH),item)

			elif len(item) == 7:
				cursor.execute('''insert or ignore into %s 
						(date, open, close, high, low, volume) values (?,?,?,?,?,?)'''
						%(tableNameH),item[0:6])
				cursor.execute('''insert or ignore into %s 
						(date, FHcontent, cqr, djr, fh_sh, nd) values (?,?,?,?,?,?)'''
						% (tableNameD), (item[0],item[6]["FHcontent"],
							item[6]["cqr"],item[6]['djr'],item[6]['fh_sh'],
							item[6]['nd']))

		conn.commit()
		cursor.close()
		conn.close()
		#print("done!")
	#price table name could be stock ID + '_HistPrice'
	def getPriceAndPutIntoDatabase(self):
		import os, sqlite3
		'''
		data in self.priceData
		values are float or int
		[{'adjclose': 6.079999923706055,
 		'close': 6.079999923706055,
 		'date': 1515115800,
 		'high': 6.110000133514404,
 		'low': 6.059999942779541,
 		'open': 6.090000152587891,
		'volume': 281784265},
		{},{},{}]
		'''
		priceData = yahooPriceParser(self.sc, self.se, self.startDate, self.stopDate).parseJson()['prices']
		sqlPath = self.dp
		conn = sqlite3.connect(sqlPath)
		cursor = conn.cursor()
		conn.commit()
		for i in range(len(priceData)):
			if 'type' in priceData[i].keys():
				tableNameD = "Dividend_" + self.sc
				cursor.execute('''create table if not exists %s 
					(date text primary key, type text, data text, amount text)''' % (tableNameD))
				try:
					cursor.execute("insert into %s (date, type, data, amount) values (?,?,?,?)"\
					 	% (tableNameD), (str(priceData[i]['date']),str(priceData[i]['type']),\
					 		str(priceData[i]['data']),str(priceData[i]['amount'])))
				except:
					#print('dividen repeat i')
					continue	
		cursor.close()
		conn.commit()
		cursor = conn.cursor()
		tableNameH = "HistPrice_" + self.sc 
		cursor.execute('''create table if not exists %s 
			(date text primary key, 
			open text, close text, high text, 
			low text, adjclose text, volume text
			)''' % (tableNameH))
		for i in range(len(priceData)):
			if 'type' not in priceData[i].keys():
				try:
					cursor.execute("insert into %s (date, open, close, high, low, adjclose, volume) values (?,?,?,?,?,?,?)"\
						% (tableNameH),(str(priceData[i]['date']),str(priceData[i]['open'])\
							,str(priceData[i]['close']),str(priceData[i]['high']),\
							str(priceData[i]['low']),str(priceData[i]['adjclose']),\
							str(priceData[i]['volume'])))
				except:
					#print("price repeat " + str(i))
					continue	
		cursor.close()
		conn.commit()
		conn.close()	

	def writeGunDongJingZhiMeiGuShouYiToDatabase(self):
		import sqlite3
		#[(报告时间，累计摊薄每股收益，每季摊薄每股收益，年末/最新摊薄每股收益，滚动摊薄每股收益),(),(),()]
		mgsy = sinaFinanParser(self.sc).getTanBoMeiGuShouYi()
		sqlPath = self.dp
		conn = sqlite3.connect(sqlPath)
		cursor = conn.cursor()
		tableNameMS = "MeiGuShouYi_" + self.sc
		cursor.execute('''create table if not exists %s
			(date text primary key,
			leiJitbsy text,
			meiJitbsy text,
			nianMoZuiXintbst text,
			gunDongtbsy text)''' % (tableNameMS))
		for i in range(len(mgsy)):
			try:
				cursor.execute('''insert into %s (date, leiJitbsy, meiJitbsy
					, nianMoZuiXintbst, gunDongtbsy) values (?,?,?,?,?)''' \
					% (tableNameMS),(mgsy[i][0],mgsy[i][1],mgsy[i][2],mgsy[i][3],mgsy[i][4]))
			except:
				print(mgsy[i])
				continue	
		cursor.close()
		conn.commit()
		conn.close()	

	def writeMeiGuJingZiChanToDatabase(self):
		import sqlite3
		#[(报告时间，每股净资产),(),(),()]
		mgjzc = sinaFinanParser(self.sc).getTiaoZhengMeiGuJingZiChan()
		sqlPath = self.dp
		conn = sqlite3.connect(sqlPath)
		cursor = conn.cursor()
		tableNameMZ = "MeiGuJingZiChan_" + self.sc
		cursor.execute('''create table if not exists %s
			(date text primary key,
			tanBojzc text)''' % (tableNameMZ))
		for i in range(len(mgjzc)):
			try:
				cursor.execute('''insert into %s (date, tanBojzc) 
					values (?,?)''' \
					% (tableNameMZ),(mgjzc[i][0],mgjzc[i][1]))
			except:
				print(mgjzc[i])
				continue	
		cursor.close()
		conn.commit()
		conn.close()	
		
	def writeFenHongFromSinaIntoDatabase(self):
		import sqlite3, json
		#[(date,{'送':0,'转':0,'派':0}),(),()]
		fh = sinaFinanParser(self.sc).getFenHongPeiSong()
		sqlPath = self.dp
		conn = sqlite3.connect(sqlPath)
		cursor = conn.cursor()
		tableNameFH = "MeiNianFenHong_" + self.sc
		cursor.execute("create table if not exists %s (date text primary key,pai text, song text, zhuan text)" %(tableNameFH))
		if len(fh[0]) > 1:
			for i in range(len(fh)):
				tmp = fh[i]
				#print(tmp)
				#print(tmp)
				#print(type(tmp))
				try:
					cursor.execute("insert into %s (date, pai, song, zhuan) values (?,?,?,?)" %(tableNameFH), (tmp[0],tmp[1]['派'],tmp[1]['送'],tmp[1]['转']))
				except Exception as e:
					#print(("insert into %s (jsonStrIn) values (?)" %(tableNameFH) + str(tmp)))
					print(self.sc + " fenHongFromSina construct error")	
					continue			
		cursor.close()
		conn.commit()
		conn.close()	

#
class updateDatabase(generalFunction):
	"""docstring for updateDatabase"""
	def __init__(self, stockCode, stockExchange='.SS', startDate = 'N', stopDate = 'N',databasePathDefault="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"):
		self.sc = stockCode
		self.se = stockExchange
		self.dp = databasePathDefault
		self.startDate = startDate
		self.stopDate = stopDate
	def stockListUpdate(self):
		getStockCodeList().insertIntoDataBase()	
	def finanXueQiuUpdate(self,dataBasePath):
		import sqlite3
		#results in {'list':[{},{}]} format
		recentFina = xueQiuPriceParser(self.sc,self.se).downloadRecentFinanDataFromXueQiu()
		if len(recentFina) < 1:
			print(self.sc + 'empty recent Prices')
		conn = sqlite3.connect(dataBasePath)
		cursor = conn.cursor()
		tableNameF = "HiistFinance_" + self.sc

		cursor.execute('''create table if not exists %s 
			(date text primary key, basiceps float
			,naps float, weightedroe float, netincgrowrate float
			,salegrossprofitrto float)''' %(tableNameF))
		for item in fina['list']:
			dateIn = item['reportdate'][0:4] + "-" + item['reportdate'][4:6] + "-" + item['reportdate'][6:8]  
			cursor.execute('''insert or ignore into %s 
				(date, basiceps, naps, weightedroe, netincgrowrate, salegrossprofitrto) 
				values (?,?,?,?,?,?)''' %(tableNameF),
				(dateIn,item['basiceps'],item['naps'],item['weightedroe'],item['netincgrowrate'],item['salegrossprofitrto']))
		conn.commit()
		cursor.close()
		conn.close()	
		

	
	def priceTencentUpdate(self):
		import sqlite3
		if self.se == '.SS':
			se = 'sh'
		elif self.se == '.SZ':
			se = 'sz'
		recentPrices = tencentPriceParser(self.sc,se).getRecentkLineData()
		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		tableNameH = "HistPrice_" + self.sc + "_tencent"
		tableNameD = "Dividend_" + self.sc + "_tencent"

		cursor.execute('''create table if not exists %s 
			(date text primary key,
			open text, close text, high text,
			 low text, volume text)'''%(tableNameH))
		cursor.execute('''create table if not exists %s
			(date text primary key, FHcontent text, cqr text,
			 djr text, fh_sh text,nd text)''' %(tableNameD))
		# on duplicate key update 报错 (sqllite has no on duplicate key update syntax)
		#on conflict == or is similar to on duplicate key
		#sqlite specific
		#http://www.sqlite.org/lang_conflict.html
		if len(recentPrices) < 1:
			print(self.sc + 'empty recent Prices')
		for item in recentPrices:
			if len(item) == 6:
				cursor.execute("""insert or ignore into %s (date, open, close, high, low, volume) values (?,?,?,?,?,?)"""
						% (tableNameH),item)

			elif len(item) == 7:
				cursor.execute('''insert or ignore into %s 
						(date, open, close, high, low, volume) values (?,?,?,?,?,?)'''
						%(tableNameH),item[0:6])
				cursor.execute('''insert or ignore into %s 
						(date, FHcontent, cqr, djr, fh_sh, nd) values (?,?,?,?,?,?)'''
						% (tableNameD), (item[0],item[6]["FHcontent"],
							item[6]["cqr"],item[6]['djr'],item[6]['fh_sh'],
							item[6]['nd']))

		conn.commit()
		cursor.close()
		conn.close()

	def priceUpdate(self):
		import sqlite3
		recentPrices = yahooPriceParser(self.sc,self.se).getRecentPrice()
		tableNameH = "HistPrice_" + self.sc
		try:
			histDate = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameH,['date'])
		except:
			print("can't get historical data!")
			return(0)
		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		dateList = []
		for item in histDate:
			dateList.append(item[0])
		for item in recentPrices:
			if 'type' in item.keys():
				tableNameD = "Dividend_" + self.sc
				cursor.execute('''create table if not exists %s 
					(date text primary key, type text, data text, amount text)''' % (tableNameD))
				try:
					cursor.execute("insert into %s (date, type, data, amount) values (?,?,?,?)"\
					 	% (tableNameD), (str(item['date']),str(item['type']),\
					 		str(item['data']),str(item['amount'])))
				except:
					#print('dividen repeat')
					continue	


			elif str(item['date']) in dateList:
				continue
			else:
				try:
					cursor.execute("insert into %s (date, open, close, high, low, adjclose, volume) values (?,?,?,?,?,?,?)"\
						% (tableNameH),(str(item['date']),str(item['open'])\
							,str(item['close']),str(item['high']),\
							str(item['low']),str(item['adjclose']),\
							str(item['volume'])))
				except:
					print("price repeat!")
					continue	
		cursor.close()
		conn.commit()
		conn.close()

	def meiGuShouYiUpdate(self):
		#sinaFinanParser(self.sc).getRecentTanBoMeiGuShouYi() 最近四季度的每股收益
		#[(报告时间，累计摊薄每股收益，每季摊薄每股收益，年末/最新摊薄每股收益，滚动摊薄每股收益),(),(),()]
		import sqlite3
		#recentMgsy from newest to oldest
		recentMgsy = sinaFinanParser(self.sc).getRecentTanBoMeiGuShouYi()	
		#recentMgsy = sinaFinanParser(self.sc).getTanBoMeiGuShouYi()
		tableNameMS = "MeiGuShouYi_" + self.sc
		try:
			histDate = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameMS,['date'])
		except:
			print("can't get historical data!")
			return(0)
		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		dateList = []
		for item in histDate:
			dateList.append(item[0])
		for i in range(len(recentMgsy)):
			#get the oldest time first
			item = recentMgsy[len(recentMgsy) - 1 - i]
			if item[0] in dateList:
				continue
			else:
				try:
					cursor.execute('''insert into %s (date, leiJitbsy, meiJitbsy
						, nianMoZuiXintbst, gunDongtbsy) values (?,?,?,?,?)''' \
						% (tableNameMS),(item[0],item[1],item[2],item[3],item[4]))
				except:
					print("meiGuShouYi repeat!")
					continue
		cursor.close()
		conn.commit()
		conn.close()
		
	def meiGuJingZiChanUpdate(self):
		#getRecentTiaoZhengMeiGuJingZiChan
		import sqlite3
		#recentMgjzc from the newest to the oldest
		recentMgjzc = sinaFinanParser(self.sc).getRecentTiaoZhengMeiGuJingZiChan()
		#recentMgjzc = sinaFinanParser(self.sc).getTiaoZhengMeiGuJingZiChan()
		#print(recentMgjzc)
		tableNameMZ = "MeiGuJingZiChan_" + self.sc
		try:
			histDate = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameMZ,['date','tanBojzc'])
		except:
			print("can't get historical data!")
			return(0)
		dateList = []
		for item in histDate:
			dateList.append(item[0])		

		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		for i in range(len(recentMgjzc)):
			#get the oldest time first
			item = recentMgjzc[-(i + 1)]
			if item in histDate:
				continue
			elif item[0] in dateList:
				cursor.execute("delete from %s where date=(?)"%tableNameMZ,(item[0],))
				cursor.execute('''insert into %s (date, tanBojzc) 
						values (?,?)''' \
						% (tableNameMZ),(item[0],item[1]))
			else:
				#generalFunction.writeIntoDatebase(self,self.dp,tableNameMZ,['date','tanBojzc'],item)
				try:
					cursor.execute('''insert into %s (date, tanBojzc) 
						values (?,?)''' \
						% (tableNameMZ),(item[0],item[1]))
				except Exception as e:
					print(self.sc + " MeiGuShouYi update error")
					continue	
		cursor.close()
		conn.commit()
		conn.close()	
		
	def fenHongFromSinaUpdate(self):
		import sqlite3, json
		#[(date,{'送':0,'转':0,'派':0}),(),()]
		fh = sinaFinanParser(self.sc).getFenHongPeiSong()
		sqlPath = self.dp
		tableNameFH = "MeiNianFenHong_" + self.sc
		if len(fh[0]) > 1:			
			try:
				histDate = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameFH,['date'])
			except:
				print("can't get historical data!")
				return(0)
			dateList = []
			for item in histDate:
				dateList.append((item[0]))

			conn = sqlite3.connect(sqlPath)
			cursor = conn.cursor()
			for i in range(len(fh)):
				if fh[i][0] in dateList:
					continue
				else:
					tmp = fh[i]
					try:				
						cursor.execute("insert into %s (date, pai, song, zhuan) values (?,?,?,?)" %(tableNameFH), (tmp[0],tmp[1]['派'],tmp[1]['送'],tmp[1]['转']))
					except Exception as e:
						#print(("insert into %s (jsonStrIn) values (?)" %(tableNameFH) + str(tmp)))
						print(self.sc + " fenHongFromSina construct error")	
						continue
			cursor.close()
			conn.commit()
			conn.close()					