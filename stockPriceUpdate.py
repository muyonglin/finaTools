import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import constructDatabase
from stock.dataSourceParse import updateDatabase
from stock.dataSourceParse import getStockCodeList

class maintainDatabase(generalFunction):
	"""docstring for maintainDatabase"""
	def __init__(self,indexFilePath = "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
		, databasePath = "D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
		,logFile = "D:/programe-data/database/stockHistInfoDatabase/update.log"):
		self.iF = indexFilePath 
		self.dp = databasePath
		self.log = logFile

	def tableNameList(self,databasePath):
		import sqlite3
		conn = sqlite3.connect(databasePath)
		cursor = conn.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tableList = cursor.fetchall()
		cursor.close()
		conn.close()
		tableNameList = []
		for item in tableList:
			tableNameList.append(item[0])
		return(tableNameList)
	def loadIndexComponent(self,filePath ):
		import json
		indexDict = json.load(open(filePath))
		#indexDict {'date':[component],'date':[],...}
		return(indexDict)


	def maintainDbAll(self):
		import datetime
		logHandle = open(self.log,'a')
		getStockCodeList()	
		stockCodeList = getStockCodeList.getListofStockCode(self)	
		uniqueStokeList1 = list(set(stockCodeList))	
		stockTableList = self.tableNameList(self.dp)
		logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")

		for item in uniqueStokeList1:
			#print("doing " + item)
			priceNameYahoo = "HistPrice_" + item[0:6]
			priceNameTencent = "HistPrice_" + item[0:6] + "_tencent"
			dividenNameYahoo = "Dividend_" + item[0:6]
			dividenNameTencent = "Dividend_" + item[0:6] + "_tencent"
			# mgsyName = "MeiGuShouYi_" + item[0:6]
			# mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			if 	priceNameTencent in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).priceTencentUpdate()
					#print("updated " + item)
				except Exception as e:
					print(item[0:6] + " price tencent")
					print(e)
					logHandle.write("can't update " + item + " price" + "\n")
					continue	
			elif priceNameYahoo in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).priceUpdate()
				except Exception as e:
					print(item[0:6] + " price Yahoo")
					print(e)
					logHandle.write("can't update " + item + " price" + "\n")
					continue
			elif priceNameYahoo not in stockTableList and priceNameTencent not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).getPriceFromTencentAndPutIntoDatabase()
					#print("constructed " + item)
				except Exception as e:
					logHandle.write("can't construct " + item + " price tencent" + "\n")
					#print(e)
					try:
						constructDatabase(item[0:6],item[6:9]).getPriceAndPutIntoDatabase()
					except Exception as e:
						print(item[0:6] + " tencent and yahoo both failed")
						print(e)
						logHandle.write("can't construct " + item + " price" + "\n")
						continue

			if priceNameTencent in stockTableList and dividenNameTencent not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).getPriceFromTencentAndPutIntoDatabase()
					#print("constructed " + item)
				except Exception as e:
					logHandle.write("can't construct " + item + " price tencent" + "\n")
					#print(e)
					try:
						constructDatabase(item[0:6],item[6:9]).getPriceAndPutIntoDatabase()
					except Exception as e:
						print(item[0:6] + " dividen tencent")
						print(e)
						logHandle.write("can't construct " + item + " price" + "\n")
						continue
			elif priceNameYahoo in stockTableList and dividenNameYahoo not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).getPriceFromTencentAndPutIntoDatabase()
					#print("constructed " + item)
				except Exception as e:
					logHandle.write("can't construct " + item + " price tencent" + "\n")
					#print(e)
					try:
						constructDatabase(item[0:6],item[6:9]).getPriceAndPutIntoDatabase()
					except Exception as e:
						print(item[0:6] + " dividen yahoo")
						print(e)
						logHandle.write("can't construct " + item + " price" + "\n")
						continue

		logHandle.close()							

if __name__ == '__main__':

	# indexFile= "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
	# database = "D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
	maintainDatabase().maintainDbAll()