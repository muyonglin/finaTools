import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import constructDatabase
from stock.dataSourceParse import updateDatabase
from stock.dataSourceParse import getStockCodeList

class maintainDatabase(generalFunction):
	"""docstring for maintainDatabase"""
	def __init__(self,indexFilePath, databasePath):
		self.iF = indexFilePath 
		self.dp = databasePath

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

	def maintainDb(self):
		getStockCodeList()
		indexDict = self.loadIndexComponent(self.iF)
		uniqueStokeList = []
		for key in indexDict:
			uniqueStokeList += indexDict[key]
		uniqueStokeList1 = list(set(uniqueStokeList))	
		stockTableList = self.tableNameList(self.dp)

		for item in uniqueStokeList1:
			priceNameYahoo = "HistPrice_" + item[0:6]
			priceNameTencent = "HistPrice_" + item[0:6] + "_tencent"
			# dividenNameYahoo = "Dividend_" + item[0:6]
			# dividenNameTencent = "Dividend_" + item[0:6] + "_tencent"
			mgsyName = "MeiGuShouYi_" + item[0:6]
			mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			if priceNameYahoo in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).priceUpdate()
				except:
					print("can't update " + item + " price")
					continue
			if 	priceNameTencent in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).priceTencentUpdate()
				except:
					print("can't update " + item + " price")
					continue		
			if priceNameYahoo not in stockTableList and priceNameTencent not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).getPriceFromTencentAndPutIntoDatabase()
				except:
					print("can't construct " + item + " price tencent")
					try:
						constructDatabase(item[0:6],item[6:9]).getPriceAndPutIntoDatabase()
					except:
						print("can't construct " + item + " price")
						continue
			if mgsyName in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).meiGuShouYiUpdate()
				except:
					print("can't update " + item + " meiGuShouYi")
					continue
			if mgsyName not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).writeGunDongJingZhiMeiGuShouYiToDatabase()
				except:
					print("can't construct " + item + "meiGuShouYi")
					continue	
			if mgjzcName in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9]).meiGuJingZiChanUpdate()
				except:
					print("can't update " + item + " meiGuJingZiChan")
					continue	
			if mgjzcName not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9]).writeMeiGuJingZiChanToDatabase()
				except:
					print("can't construct " + item + " meiGuJingZiChan")
					continue			

if __name__ == '__main__':

	indexFile= "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
	database = "D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
	maintainDatabase(indexFile,database).maintainDb()








# for item in uniqueStokeList1:
# 	if statusOfTable("HistPrice_" + item[0:6]):
# 		try:
# 			updateDatabase(item[0:6],item[6:9]).priceUpdate()
# 		except:
# 			print("can't update " + item + " price")
# 			continue			
# 	if statusOfTable("MeiGuShouYi_" + item[0:6]):
# 		try:
# 			updateDatabase(item[0:6],item[6:9]).meiGuShouYiUpdate()
# 		except:
# 			print("can't update " + item + " meiGuShouYi")
# 			continue	
# 	if statusOfTable("MeiGuJingZiChan_" + item[0:6]):
# 		try:
# 			updateDatabase(item[0:6],item[6:9]).meiGuJingZiChanUpdate()
# 		except:
# 			print("can't update " + item + " meiGuJingZiChan")
# 			continue	
# 	if not statusOfTable("HistPrice_" + item[0:6]):
# 		try:
# 			constructDatabase(item[0:6],item[6:9]).getPriceAndPutIntoDatabase()
# 		except:
# 			print("can't construct " + item + " price")
# 			continue	
# 	if not statusOfTable("MeiGuShouYi_" + item[0:6]):
# 		try:
# 			constructDatabase(item[0:6],item[6:9]).writeGunDongJingZhiMeiGuShouYiToDatabase()
# 		except:
# 			print("can't construct " + item + "meiGuShouYi")
# 			continue	
# 	if not statusOfTable("MeiGuJingZiChan_" + item[0:6]):
# 		try:
# 			constructDatabase(item[0:6],item[6:9]).writeMeiGuJingZiChanToDatabase()
# 		except:
# 			print("can't construct " + item + " meiGuJingZiChan")
# 			continue			
#can't construct table stock
#["601268.SS","603218.SS","002256.SZ","002129.SZ","300156.SZ","300187.SZ","002850.SZ","002006.SZ","603063.SS","002638.SZ","000035.SZ","300145.SZ","600187.SS","601200.SS","603588.SS"]


