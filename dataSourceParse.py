#financial data from sina financial
#http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/601398/ctrl/
#2016 #the year
#displaytype/
#4.phtml #how many quarters to display, 4 or less
#http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/601398/ctrl/2016/displaytype/4.phtml
#sina financial data is more accurate than tonghuashun
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
		for i in range(len(tmpList)):
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
		tmpFenHong_3 = []
		for item in tmpFenHong_2:
			tmp = re.findall("<td>(.*?)</td>",item)
			if tmp[5] == '--':
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

#xueqiu url
#class xueQiuPriceParser(generalFunction):

#google fianace
#https://finance.google.com/finance/historical?q=603218



#qq finance
#http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq2018&param=sh601398,day,2018-01-01,2018-12-31,320,qfq&r=0.40971276253567
#http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_day&param=sh601398,day,2016-01-01,2016-12-31,320,qfq
#http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_day&param=sh601398,day,2016-01-01,2016-12-31,365,qfq
#365 is the length of kline data list
#default data query
#http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh601398,day,,,320,qfq&r=0.05855241192611871
#use selenium and chrome headless
class tencentPriceParser(generalFunction):
	"""docstring for tencentPriceParser"""
	def __init__(self, stockCode, stockExchange='sh'):
		self.sc = stockCode
		self.se = stockExchange

	def constructURL(self):
		import datetime
		startDate = '1990'
		stopDate = str(datetime.datetime.today())[0:4]
		urlList = []
		for item in range(int(startDate),(int(stopDate) + 1)):
			url = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_day&param=" + self.se +self.sc + ",day," + str(item) + "-01-01," + str(item) + "-12-31,365,qfq"
			urlList.append(url)
		self.ull = urlList
	def getkLineData(self):
		import json
		self.constructURL()
		dataList = []
		for item in self.ull:
			html = generalFunction.tryUrl(self,item,10)
			#print(item)
			#print(html[0:50])
			#print(html[0:30])
			#print(json.loads(html[10:]))
			if json.loads(html[10:])['data'] != []:
				#dataList += json.loads(html[10:])['data'][self.se +self.sc]['qfqday']
				tmp = json.loads(html[10:])['data'][self.se +self.sc]
				if 'qfqday' in tmp.keys():
					dataList += tmp['qfqday']
		return(dataList)
	def getRecentkLineData(self):
		import json
		url = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=" + self.se +self.sc + ",day,,,320,qfq"
		html = generalFunction.tryUrl(self,url,10)
		#print(html[0:30])
		dataList = []
		if json.loads(html[13:])['data'] != []:
			tmp = json.loads(html[13:])['data'][self.se +self.sc]
			if 'qfqday' in tmp.keys():
				dataList = tmp['qfqday']
			elif 'day' in tmp.keys():
				dataList = tmp['day']	
		#dataList = json.loads(html[13:])['data'][self.se +self.sc]['qfqday']
		#print(dataList)
		return(dataList)

		
#
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
		tableNameMZ = "MeiGuJingZiChan_" + self.sc
		try:
			histDate = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameMZ,['date'])
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
			item = recentMgjzc[len(recentMgjzc) - 1 - i]
			if item[0] in dateList:
				continue
			else:
				#generalFunction.writeIntoDatebase(self,self.dp,tableNameMZ,['date','tanBojzc'],item)
				try:
					cursor.execute('''insert into %s (date, tanBojzc) 
						values (?,?)''' \
						% (tableNameMZ),(mgjzc[i][0],mgjzc[i][1]))
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
#stock list shangHai and shenZhen
#http://www.sse.com.cn/assortment/stock/list/share/
#data source file: http://www.sse.com.cn/js/common/ssesuggestfunddata.js
#					http://www.sse.com.cn/js/common/ssesuggestdataAll.js

#http://www.szse.cn/main/marketdata/jypz/colist/
#	http://www.szse.cn/szseWeb/ShowReport.szse?tab1PAGENO=4&TABKEY=tab1&CATALOGID=1110
#	tabKey 1-6 上市公司列表 A股列表 B股列表 A＋B股列表 中小企业板 创业板
#	CATALOGID 是不同证券数据 1110 是股票
#	tab1PAGENO 是页码
class getStockCodeList(generalFunction):
	"""docstring for getStockCodeList"""
	def __init__(self, databasePathDefault="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"):
		self.dp = databasePathDefault	
		self.getListofStockCode()	
		self.insertIntoDataBase()
	def shStockList(self):
		url = "http://www.sse.com.cn/js/common/ssesuggestdata.js"
		html = generalFunction.tryUrl(self,url,5,"utf-8")
		import re
		#dataList [(stockCode,中文名称),(),()...]
		dataList = re.findall("{val:\"(\d+)\",val2",html)
		dataListR = []
		for item in dataList:
			dataListR.append([str(item)])
		#print(dataListR)
		return(dataListR)
	
	def szStockList(self):
		url = "http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENO=1&ENCODE=1&TABKEY=tab1"
		generalFunction.retrieveData(self,url,'szStockList.xlsx')
		import xlrd, os
		data = xlrd.open_workbook("szStockList.xlsx")			
		table = data.sheets()[0]
		dataList = []
		for c in table.col_values(5):
			dataList.append([str(c)])
		#dataList  [('A股代码'),(),()]	
		dataListR = dataList[1:]
		os.remove("szStockList.xlsx")
		#print(dataListR)
		return(dataListR)	
	def getListofStockCode(self):
		tableNameSH = "shStockList"
		tableNameSZ = "szStockList"
		generalFunction.createTableIfNotExists(self,self.dp,tableNameSH,["stockCode text primary key"]) 
		generalFunction.createTableIfNotExists(self,self.dp,tableNameSZ,["stockCode text primary key"]) 
		shExistsData = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameSH,['stockCode'])
		szExistsData = generalFunction.fetchDataFromDatabase(self,self.dp,tableNameSZ,['stockCode'])
		#print(shExistsData)
		#print(szExistsData)
		shExistsCode = []
		szExistsCode = []
		for h in shExistsData:
			shExistsCode.append(h[0])
		for z in szExistsData:	
			szExistsCode.append(z[0])
		#print(shExistsCode)
		#print(szExistsCode)	
		#print("exist")
		self.shEC = shExistsCode
		self.szEC = szExistsCode
		#print(len(self.shEC))
		#print(len(self.szEC))
		return([s + '.SS' for s in self.shEC ]+ [s + '.SZ' for s in self.szEC])

		
	def insertIntoDataBase(self):
		sh = self.shStockList()
		sz = self.szStockList()
		#print(sh)
		#print(sz)
		#print(len(sh))
		#print(len(sz))
		shInList = []
		szInList = []
		for item1 in sh:
			if item1[0] in self.shEC or item1[0] == '':
				continue
			else:
				shInList.append(item1)
		for item2 in sz:
			if item2[0] in self.szEC or item2[0] == '':
				continue	
			else:
				szInList.append(item2)
		i = 0 
		for item in sz:
			if item[0] == "":
				i += 1
		#print(i)
		#print(szInList)
		#print(shInList)
		import sqlite3
		conn = sqlite3.connect(self.dp)
		cursor = conn.cursor()
		for item in shInList:
			try:
				cursor.execute("insert into shStockList (stockCode) values(?)",(item))
			except:
				#print("can't insert " + item[0])
				continue
		for item in szInList:
			try:
				cursor.execute("insert into szStockList (stockCode) values(?)",(item))
			except:
				#print("can't insert " + item[0])
				continue				
		cursor.close()
		conn.commit()
		conn.close()		

					
				




#can collect index data from joinQuant
#store index components in file, json format
#