#test strategies of selecting stocks

#testing methods for Guxilv strategy
#1, construct matrix (pandas dataframe) of historical PB and Guxilv for every stocks
#2, save matrix to a file in json format
#3, select stocks satisfy the standard as time goes down
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import getStockCodeList
from stock.stockManipulation import backTest



def testAllStocks():
	import datetime 
	logHandle = open("D:/programe-data/database/stockHistInfoDatabase/backTest.log",'a')
	stockCodeList = getStockCodeList().getListofStockCode()	
	uniqueStokeList1 = list(set(stockCodeList))	
	logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")
	resultHandle = open("D:/programe-data/database/stockHistInfoDatabase/backTest.result",'w')
	#print(len(uniqueStokeList1))
	resultDict = {}
	i = 0
	tradingDays = generalFunction().getTradingDays()
	tradingDaysDt = [datetime.datetime.strptime(item,"%Y-%m-%d") for item in tradingDays]
	tradingDaysDtFrom20000101 = []
	for item in tradingDaysDt:
		if item > datetime.datetime.strptime('2000-1-1','%Y-%m-%d'):
			tradingDaysDtFrom20000101.append(item)
	#fast test whole pipeline
	#for item in uniqueStokeList1[:30]:
	for item in uniqueStokeList1:
		#print(item)
		#print(resultDict)
		try:
			resultDict1 = backTest(item[0:6]).testForOneStock(resultDict,tradingDaysDtFrom20000101)
		except Exception as e:
			print(item[0:6] + " select error " + str(e))
			logHandle.write(item[0:6] + " select error " + str(e) + " \n")
			resultDict1 = resultDict
			continue
		resultDict = resultDict1
		i += 1 
		print(str(i) + " : " + item[0:6] + " done!")	
	#print(list(resultDict.keys()))
	#dateList = list(resultDict.keys())
	end = datetime.datetime.today()
	start = datetime.datetime.strptime('2000-1-1','%Y-%m-%d')	
	td = datetime.timedelta(days=1)	
	dtList = []
	while start < end:
		start += td
		if start in tradingDaysDt:
			dtList.append(start)

	dateList = dtList
	dateList.sort()
	#print(dateList)
	for item in dateList:
		if item not in resultDict.keys():
			resultHandle.write(str(item.date()) + ":\n")
		else: 
			resultHandle.write(str(item.date()) + ":\t")
			resultHandle.write("\t".join(resultDict[item]) + "\n")
	logHandle.close()
	resultHandle.close()
	
if __name__ == '__main__':
	testAllStocks()
	
			
