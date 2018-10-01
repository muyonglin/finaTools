import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import constructDatabase
from stock.dataSourceParse import updateDatabase
from stock.dataSourceParse import getStockCodeList

class maintainDatabase(generalFunction):
	"""docstring for maintainDatabase"""
	def __init__(self, databasePath = "D:/programe-data/database/stockHistInfoDatabase/xueQiuFinanInfo.db"
		,logFile = "D:/programe-data/database/stockHistInfoDatabase/xueQiufinanUpdate.log"):
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

	def maintainDbAll(self):
		import datetime
		logHandle = open(self.log,'a')
		getStockCodeList(self.dp)	
		stockCodeList = getStockCodeList(self.dp).getListofStockCode()	
		uniqueStokeList1 = list(set(stockCodeList))	
		stockTableList = self.tableNameList(self.dp)
		#print(stockTableList)
		print(len(uniqueStokeList1))
		logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")
		self.updateXueQiuFina(uniqueStokeList1,stockTableList,logHandle)
		logHandle.close()

	def updateXueQiuFina(self,uniqueStokeList,stl,logH):
		logHandle = logH
		stockTableList = stl
		uniqueStokeList1 = uniqueStokeList
		for item in uniqueStokeList1:
			#print("doing " + item)
			tableNameF = "HiistFinance_" + item[0:6]
			#mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			#fhName = "MeiNianFenHong_" + item[0:6]
			if tableNameF in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9],'N','N',self.dp).finanXueQiuUpdate(self.dp)
					#print('updated mgsy ' + item)
				except Exception as e:
					print(item[0:6] + " xueQiuFian update")
					print(e)
					logHandle.write("can't update " + item + " xueQiuFian" + "\n")
					continue
			elif tableNameF not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9],'N','N',self.dp).getFianFromXueQiuAndWriteIntoDatabase(self.dp)
					#print('constrcted mgsy ' + item)
				except Exception as e:
					print(item[0:6] + " xueQiuFian construct")
					print(e)
					logHandle.write("can't construct " + item + "xueQiuFian" + "\n")
					continue
if __name__ == '__main__':

	# indexFile= "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
	# database = "D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
	maintainDatabase().maintainDbAll()
