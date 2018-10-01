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
from stock.unusedCode.deprecatedClasses import sinaFinanParser, yahooPriceParser

#xueqiu url
#雪球 
# 股票信息 
# https://xueqiu.com/stock/f10/compinfo.json?symbol=SZ000501 
# 利润表 
# https://xueqiu.com/stock/f10/incstatement.json?symbol=SZ000501 
# 资产负债表 
# https://xueqiu.com/stock/f10/balsheet.json?symbol=SZ000501 
# 现金流量表 
# https://xueqiu.com/stock/f10/cfstatement.json?symbol=SZ000501&size=10000&page=1 
# 行情 
# https://xueqiu.com/stock/forchartk/stocklist.json?period=1d&type=normal&symbol=SZ000001 
# 分红 
# https://xueqiu.com/stock/f10/bonus.json?symbol=SZ000501&size=10000&page=1 
# 行业 
# https://xueqiu.com/industry/quote_order.json?page=1&size=10000&order=desc&exchange=CN&orderBy=percent&level2code=J68

#class xueQiuPriceParser(generalFunction):
#xueqiu finance data (json sormat)
#https://xueqiu.com/stock/f10/finmainindex.json?symbol=SH600107&page=1&size=1000&


class xueQiuPriceParser(generalFunction):
	"""docstring for xueQiuPriceParser"""
	def __init__(self,stockCode,stockExchange=".SH"):
		super(xueQiuPriceParser, self).__init__()
		self.sc = stockCode
		self.se = stockExchange
		

	def downloadAllFinanDataFromXueQiu(self):
		import requests, json, time
		url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=" + \
			self.se[1:].upper() + self.sc + "&page=1&size=1000"
		headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			#'Accept-Encoding': 'gzip, deflate, br'
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'cache-control': 'no-cache',
			'Connection': 'keep-alive',
			'Cookie': 's=ed11s5yfko; device_id=7a9a3167a71703b9be6fa72ea08fa695; bid=be9085a54839477beb13d93d69e09efe_j8zahgg0; webp=0; _ga=GA1.2.688642971.1508466899; __utmz=1.1537413750.582.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gid=GA1.2.290465721.1537799219; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=5b35c20489b117b78da31bfd63086c0311b263c2; xq_a_token.sig=jVwh4Lvwf_doVvSUfGv6Xc3PK-s; xqat=5b35c20489b117b78da31bfd63086c0311b263c2; xqat.sig=XKojjoeQARK8wtl3EuI7TYkW0Kc; xq_r_token=b20e94a034fe7ddacdd8843afc66c0209a565b92; xq_r_token.sig=p01A1xVYZZv1tUOL70asQ5rDYXo; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=8247314677; u.sig=IQn-4EKHa9ff8engyOBqjVJNLyY; Hm_lvt_fe218c11eab60b6ab1b6f84fb38bcc4a=1535895476,1538041998; aliyungf_tc=AQAAAJC2GBY6GwIAIRR/yufgpgU9dtur; Hm_lvt_1db88642e346389874251b5a1eded6e3=1538355512,1538355848,1538360210,1538379663; __utma=1.688642971.1508466899.1538367360.1538379671.599; __utmc=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1538382895; __utmt=1; __utmb=1.15.10.1538379671',
			'Host': 'xueqiu.com',
			'Referer': 'https://xueqiu.com/S/SH601107/ZYCWZB',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest'

		}
		try:
			res = requests.get(url,headers=headers)
			time.sleep(20)
			#results format {'list':[{},{}]}
			#from newest to oldest
			results = json.loads(res.text)
			return(results)
		except Exception as e:
			print("xueQiu Download error: " + self.sc + self.se + " " + str(e))	
			time.sleep(20)
			return(0)
	def downloadRecentFinanDataFromXueQiu(self):
		import requests, json, time
		url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=" + \
			self.se[1:].upper() + self.sc + "&page=1&size=4&"
		headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			#'Accept-Encoding': 'gzip, deflate, br'
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
			'cache-control': 'no-cache',
			'Connection': 'keep-alive',
			'Cookie': 's=ed11s5yfko; device_id=7a9a3167a71703b9be6fa72ea08fa695; bid=be9085a54839477beb13d93d69e09efe_j8zahgg0; webp=0; _ga=GA1.2.688642971.1508466899; __utmz=1.1537413750.582.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gid=GA1.2.290465721.1537799219; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=5b35c20489b117b78da31bfd63086c0311b263c2; xq_a_token.sig=jVwh4Lvwf_doVvSUfGv6Xc3PK-s; xqat=5b35c20489b117b78da31bfd63086c0311b263c2; xqat.sig=XKojjoeQARK8wtl3EuI7TYkW0Kc; xq_r_token=b20e94a034fe7ddacdd8843afc66c0209a565b92; xq_r_token.sig=p01A1xVYZZv1tUOL70asQ5rDYXo; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=8247314677; u.sig=IQn-4EKHa9ff8engyOBqjVJNLyY; Hm_lvt_fe218c11eab60b6ab1b6f84fb38bcc4a=1535895476,1538041998; aliyungf_tc=AQAAAJC2GBY6GwIAIRR/yufgpgU9dtur; Hm_lvt_1db88642e346389874251b5a1eded6e3=1538355512,1538355848,1538360210,1538379663; __utma=1.688642971.1508466899.1538367360.1538379671.599; __utmc=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1538382895; __utmt=1; __utmb=1.15.10.1538379671',
			'Host': 'xueqiu.com',
			'Referer': 'https://xueqiu.com/S/SH601107/ZYCWZB',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest'

		}
		try:
			res = requests.get(url,headers=headers)
			time.sleep(5)
			#results format {'list':[{},{}]}
			#from newest to oldest
			results = json.loads(res.text)
			return(results)
		except Exception as e:
			print("xueQiu Download error: " + self.sc + self.se + " " + str(e))	
			time.sleep(5)
			return(0)


			

		
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
		
#use tushare get eps
class tushareDataParse(generalFunction):
	"""use tushare get eps data
	   put eps into finan database
	"""
	def __init__(self, arg):
		super(tushareDataParse, self).__init__()
		self.arg = arg
	def getEps():
		pass

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