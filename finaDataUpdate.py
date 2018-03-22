import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import constructDatabase
from stock.dataSourceParse import updateDatabase
from stock.dataSourceParse import getStockCodeList


class maintainDatabase(generalFunction):
	"""docstring for maintainDatabase"""
	def __init__(self,indexFilePath = "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
		, databasePath = "D:/programe-data/database/stockHistInfoDatabase/stockFinanInfo.db"
		,logFile = "D:/programe-data/database/stockHistInfoDatabase/finanUpdate.log"):
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
		getStockCodeList(self.dp)	
		stockCodeList = getStockCodeList(self.dp).getListofStockCode()	
		uniqueStokeList1 = list(set(stockCodeList))	
		stockTableList = self.tableNameList(self.dp)
		#print(stockTableList)
		print(len(uniqueStokeList1))
		logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")
		print(sys.argv)
		if len(sys.argv) < 2:
			self.updateMgsy(uniqueStokeList1,stockTableList,logHandle)
			self.updateMgjzc(uniqueStokeList1,stockTableList,logHandle)
			self.updateSinaFh(uniqueStokeList1,stockTableList,logHandle)
		else:			
			if 'fh' in sys.argv[1:]:
				self.updateSinaFh(uniqueStokeList1,stockTableList,logHandle)
			if 'mgsy' in sys.argv[1:]:
				self.updateMgsy(uniqueStokeList1,stockTableList,logHandle)
			if "mgjzc" in sys.argv[1:]:
				self.updateMgjzc(uniqueStokeList1,stockTableList,logHandle)	
		logHandle.close()

	def updateMgsy(self,uniqueStokeList,stl,logH):
		logHandle = logH
		stockTableList = stl
		uniqueStokeList1 = uniqueStokeList
		for item in uniqueStokeList1:
			#print("doing " + item)
			mgsyName = "MeiGuShouYi_" + item[0:6]
			#mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			#fhName = "MeiNianFenHong_" + item[0:6]
			if mgsyName in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9],'N','N',self.dp).meiGuShouYiUpdate()
					#print('updated mgsy ' + item)
				except Exception as e:
					print(item[0:6] + " mgsy update")
					print(e)
					logHandle.write("can't update " + item + " meiGuShouYi" + "\n")
					continue
			elif mgsyName not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9],'N','N',self.dp).writeGunDongJingZhiMeiGuShouYiToDatabase()
					#print('constrcted mgsy ' + item)
				except Exception as e:
					print(item[0:6] + " mgsy construct")
					print(e)
					logHandle.write("can't construct " + item + "meiGuShouYi" + "\n")
					continue
	def updateMgjzc(self,uniqueStokeList,stl,logH):
		logHandle = logH
		stockTableList = stl
		uniqueStokeList1 = uniqueStokeList			
		for item in uniqueStokeList1:
			#print("doing " + item)
			#mgsyName = "MeiGuShouYi_" + item[0:6]
			mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			#fhName = "MeiNianFenHong_" + item[0:6]	
			if mgjzcName in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9],'N','N',self.dp).meiGuJingZiChanUpdate()
					#print("updated mgjzc " + item)
				except Exception as e:
					print(item[0:6] + " mgjzc update")
					print(e)
					logHandle.write("can't update " + item + " meiGuJingZiChan" + "\n")
					continue	
			elif mgjzcName not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9],'N','N',self.dp).writeMeiGuJingZiChanToDatabase()
					#print('constrcted mgjzc ' + item)
				except Exception as e:
					print(item[0:6] + " mgjzc construct")
					print(e)
					logHandle.write("can't construct " + item + " meiGuJingZiChan" + "\n")
					continue
	def updateSinaFh(self,uniqueStokeList,stl,logH):
		logHandle = logH
		stockTableList = stl
		uniqueStokeList1 = uniqueStokeList			
		for item in uniqueStokeList1:
			#print("doing " + item)
			#mgsyName = "MeiGuShouYi_" + item[0:6]
			#mgjzcName = "MeiGuJingZiChan_" + item[0:6]
			fhName = "MeiNianFenHong_" + item[0:6]			
			if fhName in stockTableList:
				try:
					updateDatabase(item[0:6],item[6:9],'N','N',self.dp).fenHongFromSinaUpdate()
					#print("updated mgjzc " + item)
				except Exception as e:
					print(item[0:6] + ' fh update')
					print(e)
					logHandle.write("can't update " + item + " fenHongFromSina" + "\n")
					continue	
			elif fhName not in stockTableList:
				try:
					constructDatabase(item[0:6],item[6:9],'N','N',self.dp).writeFenHongFromSinaIntoDatabase()
					#print('constrcted mgjzc ' + item)
				except Exception as e:
					print(item[0:6] + " fh construct")
					print(e)
					logHandle.write("can't construct " + item + " fenHongFromSina" + "\n")
					continue			

							

if __name__ == '__main__':

	# indexFile= "D:/programe-data/database/stockHistInfoDatabase/000827_index_components.txt"
	# database = "D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
	maintainDatabase().maintainDbAll()