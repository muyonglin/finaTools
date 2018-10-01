#test the buying and selling strategy based on bact test result
#testing strategy: 
#emulate an account with 1,000,000 RMB at the beging
#
%load_ext autoreload
%autoreload 2

import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import getStockCodeList
from stock.stockManipulation import backTest, tradeStock, stockInfoManipulation

def portfolioBackTest():
	#1，get list of stock that can be bought
	#2, get the selling date for all bought stock
	#3, loop along the time (every week), update portforlio
	import datetime
	logHandle = open("D:/programe-data/database/stockHistInfoDatabase/portfolioBackTest.log",'a')
	stockCodeList = getStockCodeList().getListofStockCode()	
	uniqueStokeList1 = list(set(stockCodeList))	
	logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")
	resultHandle = open("D:/programe-data/database/stockHistInfoDatabase/portfolioBackTest.result",'w')
	#print(len(uniqueStokeList1))
	#fast test whole pipeline
	#for item in uniqueStokeList1[:30]:	
	
	#1, all bought stocks 
	buyDict = {}
	i = 0
	for item in uniqueStokeList1:
		#print(item)
		#print(buyDict)
		try:
			buyDict1 = backTest(item[0:6]).testForOneStock(buyDict)
		except Exception as e:
			print(item[0:6] + " select error " + str(e))
			logHandle.write(item[0:6] + " select error " + str(e) + " \n")
			buyDict1 = buyDict
			continue
		buyDict = buyDict1
		i += 1 
		print(str(i) + " : " + item[0:6] + " done!")	

	#check bought stocks	
	stockBought = list(set([item for sublist in buyDict.values() for item in sublist]))

	#2, selling date
	sellingDict = {}
	i = 0
	for item in stockBought:
		try:
			sellingDict1 = backTest(item[0:6]).testForSell(sellingDict)
		except Exception as e:
			print(item[0:6] + " sell error " + str(e))
			logHandle.write(item[0:6] + " sell error " + str(e) + " \n")
			sellingDict1 = sellingDict
			continue
		sellingDict = sellingDict1
		i += 1 
		print(str(i) + " : " + item[0:6] + " done!")	

	#3, loop for all days
	#generalFunction().getTradingDays()
	#without brace, don't need self when define the method
	tradingDays = generalFunction().getTradingDays()
	# tradingDaysDt = [datetime.datetime.strptime(item,"%Y-%m-%d") for item in tradingDays]
	# buyDate = [generalFunction().getNearestDate(tradingDaysDt,item) for item in list(buyDict.keys())]
	# sellDate =[generalFunction().getNearestDate(tradingDaysDt,item) for item in list(sellingDict.keys())] 
	#buyDateBack = [stockInfoManipulation.getNearestDateBack(list(buyDict.keys()),item) for item in buyDate]
	portfolioDict = {"cash":1000000,"stock":{},"totalCapital":1000000}
	valueChange = [portfolioDict]

	for item in tradingDays:
		today = datetime.datetime.strptime(item,"%Y-%m-%d")
		buyStockInfo = []
		sellStockInfo = []
		holdStockInfo = []
		if today in buyDict.keys():
			for stockID in buyDict[today]:
				tmp = stockInfoManipulation().fetchStockInfo([stockID],['date',"'" + item + "'"],['close'])
				buyStockInfo.append((stockID,tmp[0][0][0]))
		if today in sellingDict.keys():
			for stockID in sellingDict[today]:
				tmp = stockInfoManipulation().fetchStockInfo([stockID],['date',"'" + item + "'"],['close'])
				sellStockInfo.append((stockID,tmp[0][0][0]))
		if today in buyDict.keys() or today in sellingDict.keys():
			if len(list(portfolioDict['stock'].keys())) > 0:
				for holdStockID in portfolioDict['stock'].keys():
					tmp = stockInfoManipulation().fetchStockInfo([holdStockID],['date',"'" + item + "'"],['close'])
					if tmp == [[]]:
						continue
					else:
						holdStockInfo.append((holdStockID,tmp[0][0][0]))

			# print("portforlioTmp")
			# print(portfolioDict)
			# print(portforlioTmp)
			portforlioTmp = tradeStock(buyStockInfo,sellStockInfo,holdStockInfo).portfolioAdjustment(resultHandle,portfolioDict)		

			if portforlioTmp['cash'] != portfolioDict['cash']:
				# print("portforlioTmp")
				print(portforlioTmp)
				resultHandle.write(item + str(portforlioTmp))
				valueChange.append((item,portforlioTmp))
				portfolioDict = portforlioTmp
				# print("portfolioDict")
				# print(portfolioDict)
	logHandle.close()
	resultHandle.close()

	

if __name__ == '__main__':

