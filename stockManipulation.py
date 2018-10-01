###############################################################################################
#
#functions for buy, sell, judge stocks
#
###############################################################################################
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
class backTest(generalFunction):
	"""docstring for backTest"""
	def __init__(self, stockCode,startDate='2000-1-1'
		, calDatabase='D:/programe-data/database/stockHistInfoDatabase/calInfo.db'):
		super(backTest, self).__init__()
		self.sc = stockCode
		self.dc = calDatabase
		self.sad = startDate

	def getPBGXLData(self):
		tableName = "HistCal_" + self.sc
		try:
			PB_GXL = generalFunction.fetchDataFromDatabase(self,self.dc,tableName,['date','PB','guxilv'])
			#PB_GXL, from oldest to today
			PB_GXL.sort(key=lambda tup: tup[0])
		except Exception as e:
			print('Hist PB_GXL ' + self.sc + str(e))
			PB_GXL = 0
		return(PB_GXL)	

	def dateSeries(self):
		import datetime as dt
		end = dt.datetime.strptime(self.sod,'%Y-%m-%d')
		start = dt.datetime.strptime(self.sad,'%Y-%m-%d')
		
		td = dt.timedelta(days=1)	
		dtList = []
		while start < end:
			start += td
			if start.weekday() == 6:
				dtList.append(start)
		return(dtList)		

	def getNearestDate(self,dateList,targetDate):
		import datetime as dt
		#print(targetDate)
		for i in range(0,(len(dateList)-1)):
			if targetDate >= dateList[i] and targetDate < dateList[i+1]:
				return(dateList[i])
			elif targetDate >= dateList[-1]:
				return(dateList[-1])
	def selectStocks(self,histDataDF):
		#begin test only when stocks has more than 3 years of data
		if len(histDataDF) < 840:
			return(False)
		elif (histDataDF.iloc[:,2] == 0).sum()/len(histDataDF.iloc[:,2]) > 0.1:	
			return(False)
		else:
			#GXL higher than 90% and > 3%, PB lower than 90%
			#print(histDataDF.iloc[:,2].quantile(0.9))
			if histDataDF.iloc[-1,2] > histDataDF.iloc[:,2].quantile(0.9) and histDataDF.iloc[-1,2] > 0.03 and histDataDF.iloc[-1,1] < histDataDF.iloc[:,1].quantile(0.1) and histDataDF.iloc[-1,1] < 1:
				return(True)
			else:
				return(False)
								

	def testForOneStock(self,resultDict={},dateRange=[]):
		PB_GXL = self.getPBGXLData()
		if PB_GXL == 0:
			return(resultDict)
		#data time longer than 3 years	
		elif len(PB_GXL) > 840:
			#print(resultDict)
			import pandas as pd
			import datetime as dt
			dateList = [dt.datetime.strptime(i[0],"%Y-%m-%d") for i in PB_GXL]
			#print(dateList)
			self.sod = PB_GXL[-1][0]
			if dateRange == []:
				dateRange = self.dateSeries()	
			PB_GXL_df = pd.DataFrame(PB_GXL)
			#PB_GXL_df.iloc[:,0] = pd.to_datetime(PB_GXL_df.iloc[:,0])
			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 
			#buy after 560 days of IPO
			timeAfterIPO = dt.timedelta(days=560)	
			for item in dateRange:
				if item > (dateList[0] + timeAfterIPO):					
					# print(item)
					endDate = self.getNearestDate(dateList,item)
					# print(endDate)
					dateIndex = dateList.index(endDate)
					dataForTest = PB_GXL_df.iloc[0:dateIndex,:]
					if self.selectStocks(dataForTest):
						if item in resultDict.keys():
							resultDict[endDate].append(self.sc)
						else:
							resultDict[endDate] = [self.sc]
			return(resultDict)
		else:
			return(resultDict)

	def onlyTestLatestTime(self):
		PB_GXL = self.getPBGXLData()
		if PB_GXL == 0:
			return(0)
		else:	
			import pandas as pd
			PB_GXL_df = pd.DataFrame(PB_GXL)
			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 			
			#print(PB_GXL_df)	
			if self.selectStocks(PB_GXL_df):
				return(self.sc)
			else:
				return(0)	

	def selectStockForSell(self,histDataDF):
		#bought stock already saturate all the requirment
		#sell when PB is higher than 70% times
		if histDataDF.iloc[-1,1] > histDataDF.iloc[:,1].quantile(0.7):
			return(True)
		else:
			return(False)
				
	def testForSell(self,resultDict={}):
		PB_GXL = self.getPBGXLData()
		if PB_GXL == 0:
			return(0)
		elif len(PB_GXL) > 840:
			import pandas as pd
			import datetime as dt
			dateList = [dt.datetime.strptime(i[0],"%Y-%m-%d") for i in PB_GXL]
			#print(dateList)
			self.sod = PB_GXL[-1][0]		
			dateRange = self.dateSeries()
			PB_GXL_df = pd.DataFrame(PB_GXL)
			PB_GXL_df.iloc[:,1] = pd.to_numeric(PB_GXL_df.iloc[:,1])
			PB_GXL_df.iloc[:,2] = pd.to_numeric(PB_GXL_df.iloc[:,2]) 

			#buy after 560 days of IPO
			timeAfterIPO = dt.timedelta(days=560)	
			for item in dateRange:
				if item > (dateList[0] + timeAfterIPO):					
					#print(item)
					endDate = self.getNearestDate(dateList,item)
					#print(endDate)
					dateIndex = dateList.index(endDate)
					dataForTest = PB_GXL_df.iloc[0:dateIndex,:]
					if self.selectStockForSell(dataForTest):
						if item in resultDict.keys():
							resultDict[endDate].append(self.sc)
						else:
							resultDict[endDate] = [self.sc]
			return(resultDict)
			
class tradeStock(generalFunction):
	"""portfolioState: {"cash":float,
						"stock":{'stockID1':(stockAmount,buyingPrice,currentPrice),'stockID2':(stockAmount,buyingPrice,currentPrice),,,},
						"totalCapital":float}
		buyStockInfoList:  [(stockID1,closePrice),(stockID2,closePrice),,,]
		sellStockInfoList: [(stockID1,closePrice),(stockID2,closePrice),,,]
		holdingStockInfoList: [(stockID1,closePrice),(stockID2,closePrice),,,]
		type(stockID) == str
		type(closePrice) == str
		type(stockAmount) == int
		use 5% of total cash to buy new stocks
						"""
	def __init__(self, buyStockInfoList=[], sellStockInfoList=[],holdingStockInfoList=[]):
		# self.pS = portfolioState
		self.bf = buyStockInfoList
		self.sf = sellStockInfoList
		self.hs = holdingStockInfoList

	def portfolioAdjustment(self, resultHandle,portfolioState={"cash":1000000,"stock":{},"totalCapital":1000000}):
		import copy
		refreshedPortfolioTmp = copy.deepcopy(portfolioState)
		if len(self.hs) != 0:
			refreshedPortfolio = self.refreshPortfolio(refreshedPortfolioTmp)
			refreshedPortfolioTmp = refreshedPortfolio
		if len(self.sf) != 0:
			refreshedPortfolio = self.sellStock(refreshedPortfolioTmp,resultHandle,self.sf)
			refreshedPortfolioTmp = refreshedPortfolio
		if len(self.bf) != 0 :
			refreshedPortfolio = self.buyStock(refreshedPortfolioTmp,self.bf)
		# print(portfolioState)
		# print(refreshedPortfolio)
		return(refreshedPortfolio)	


	def buyStock(self, portfolioInfo, buyStockInfo = []):
		#cashAmount and stockPrice should be float
		if len(portfolioInfo["stock"].keys()) >= 20:
			cashAmount = 0
		else:
			cashAmount = portfolioInfo["cash"] / (20 - len(portfolioInfo["stock"].keys()))
		stockAmount = 0
		buyCash = 0
		for item in buyStockInfo:
			if item[0] in portfolioInfo['stock'].keys():
				continue
			else:				
				stockAmount = ((cashAmount / float(item[1])) // 100) * 100
				buyCash += float(item[1]) * stockAmount
				portfolioInfo['stock'][item[0]] = (stockAmount,item[1],item[1])
		portfolioInfo["cash"] -= buyCash 
		# print("after buy")
		# print(portfolioInfo)
		return(portfolioInfo)	

	def sellStock(self, portfolioInfo, resultHandle,sellingStockInfo=[]):
		soldCash = 0
		for item in sellingStockInfo:
			if item[0] in portfolioInfo['stock'].keys():
#				print(portfolioInfo['stock'][item[0]])
				soldCash += float(portfolioInfo['stock'][item[0]][0]) * float(item[1])
				print(portfolioInfo['stock'][item[0]])
				resultHandle.write(str(portfolioInfo['stock'][item[0]]))
				del portfolioInfo['stock'][item[0]]
		portfolioInfo['cash'] += soldCash
		# print("after sell")
		# print(portfolioInfo)
		return(portfolioInfo)

	def refreshPortfolio(self,portfolioIn):
		stockValue = 0
		outDict = portfolioIn
		# print("outdict")
		# print(portfolioIn)
		# print(outDict)
		for item in self.hs:
			tmp = outDict['stock'][item[0]]
			# print(tmp)
			outDict['stock'][item[0]] = (tmp[0],tmp[1],item[1])
			stockValue += int(tmp[0]) * float(item[1])
		outDict['totalCapital'] = outDict['cash'] + stockValue
		# print("after refresh")
		# print(outDict)
		return(outDict)	
	
class stockInfoManipulation(generalFunction):
	"""docstring for stockInfoManipulation"""
	def __init__(self):
		super(stockInfoManipulation, self).__init__()

	def getNearestDate(dateList,targetDate):
		import datetime as dt
		#print(targetDate)
		for i in range(0,(len(dateList)-1)):
			if targetDate >= dateList[i] and targetDate < dateList[i+1]:
				return(dateList[i])	
	def getNearestDateBack(dateList,targetDate):
		import datetime as dt
		#print(targetDate)
		for i in range(1,(len(dateList))):
			if targetDate <= dateList[i] and targetDate > dateList[i-1]:
				return(dateList[i])	
			
	def fetchStockInfo(self,stockCodeList,primaryID,colName,databasePath="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"):
		#primaryID: ['date','2000-1-1']
		tmp = []
		for item in stockCodeList:
			tableName = "HistPrice_" + item + "_tencent"
			fetchData = generalFunction.fetchDataByID(self,databasePath,tableName,primaryID,colName)
			tmp.append(fetchData)
		return(tmp)	
