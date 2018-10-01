#store calculation result into a database
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.calculation import calculatePEPB
from stock.dataSourceParse import getStockCodeList
from stock.back_test import backTest
class constructDatabaseForCalculation(generalFunction):
	"""stockCode is a string"""
	def __init__(self, stockCode
		,calculationDatabase='D:/programe-data/database/stockHistInfoDatabase/calInfo.db'):
		super(constructDatabaseForCalculation, self).__init__()
		self.sc = stockCode
		self.dpc = calculationDatabase

	def mergePBGXL(self):
		#PB data is shorter than GXL data
		#PB data begins after the first mgjzc reported
		#GXL data begins after the first price generated
		try:
			HistPB = calculatePEPB(self.sc).calculatePB()
		except Exception as e:
			print("Hist PB " + self.sc + " " + str(e))
			HistPB = 0
		try:
			HistGXL = calculatePEPB(self.sc).calculateGuXiLv()
		except Exception as e:
			print("Hist GXL " + self.sc + " " + str(e))
			HistGXL = 0

		if HistPB == 0:
			return(0)
		elif HistPB != 0 and HistGXL == 0:
			HistPB.sort(key=lambda tup: tup[0])

			tmpList = []
			for i in range(len(HistPB)):
				tmpList.append((HistPB[i][0],HistPB[i][1],0))			
			return(tmpList)
		else:		
			#PB, GXL  from oldest to newest
			HistPB.sort(key=lambda tup: tup[0])
			HistGXL.sort(key=lambda tup: tup[0])

			tmpGXL = [(i[0],i[1]) for i in HistGXL]
			GXLDict = dict(tmpGXL)

			tmpList = []
			for i in range(len(HistPB)):
				if HistPB[i][0] in GXLDict.keys():
					tmpList.append((HistPB[i][0],HistPB[i][1],GXLDict[HistPB[i][0]]))
				else:
					print("no GXL at " + HistPB[i][0])				
			return(tmpList)	

	def writeHistPBGXLIntoDataBase(self):
		#[date,PB]
		HistPB_GXL = self.mergePBGXL()
		if HistPB_GXL == 0:
			return(0)
		else:
			import sqlite3
			conn = sqlite3.connect(self.dpc)
			cursor = conn.cursor()
			tableName = "HistCal_" + self.sc
			cursor.execute('''create table if not exists %s
				(date text primary key, PB text,guxilv text)''' % (tableName))
			for item in HistPB_GXL:
				if len(item)==3:
					cursor.execute('''insert into %s (date, PB, guxilv) values(?,?,?)''' %(tableName),item)
				else:
					print("not (date,PB,guxilv)")
			conn.commit()
			cursor.close()
			conn.close()
	def updateHistPBGXLDatabase(self):
		tableName = "HistCal_" + self.sc
		HistPB_GXL = self.mergePBGXL()
		if HistPB_GXL == 0:			
			return(0)
		else:	
			try:
				HistPB_GXL_d = generalFunction.fetchDataFromDatabase(self,self.dpc,tableName,['date','PB','guxilv'])
			except:
				print("can't fetch Hist PB data for " + tableName)
				return(0)
			dateList=[]	
			for item in HistPB_GXL_d:
				dateList.append(item[0])

			import sqlite3
			conn = sqlite3.connect(self.dpc)
			cursor = conn.cursor()
			for item in HistPB_GXL:
				if item in HistPB_GXL_d:
					continue
				elif item[0] in dateList:
					cursor.execute("delete from %s where date=(?)"%tableName,(item[0],))
					cursor.execute('''insert into %s (date, PB, guxilv) values(?,?,?)''' %(tableName),item)
				else:			
					if len(item)==3:
						#cursor.execute('''insert into %s (date, PB) values(?,?)''' %(tableNameP),item)
						cursor.execute('''insert into %s (date, PB, guxilv) values(?,?,?)''' %(tableName),item)

					else:
						print("not (date,PB,guxilv)")
			conn.commit()
			cursor.close()
			conn.close()
def tableNameList(databasePath):
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
if __name__ == '__main__':
	import datetime
	calculationDatabase='D:/programe-data/database/stockHistInfoDatabase/calInfo.db'
	priceDatabasePath="D:/programe-data/database/stockHistInfoDatabase/stockFinanInfo.db"
	logHandle = open("D:/programe-data/database/stockHistInfoDatabase/calInfo.log",'a')
	stockCodeList = getStockCodeList().getListofStockCode()
	uniqueStokeList1 = list(set(stockCodeList))
	stockTableList = tableNameList(calculationDatabase)			
	logHandle.write(str(datetime.datetime.today()) + " " + str(len(uniqueStokeList1)) + " stock codes\n")
	
	for item in uniqueStokeList1:
		tableName = "HistCal_" + item[0:6]
		if tableName in stockTableList:
			try:
				constructDatabaseForCalculation(item[0:6]).updateHistPBGXLDatabase()
			except Exception as e:
				print(item[0:6] + " hist PB_GXL update error: " + str(e))
				logHandle.write("can't update " + item + " hist PB " + "\n")
				continue
		elif tableName not in stockTableList:
			try:
				constructDatabaseForCalculation(item[0:6]).writeHistPBGXLIntoDataBase()
			except Exception as e:
				print(item[0:6] + " hist PB_GXL write error: " + str(e))
				logHandle.write("can't write " + item + " hist PB " + "\n")
				continue
	logHandle.close()	

	calResHandle = open("D:/programe-data/database/stockHistInfoDatabase/HighGXLLowPB.txt",'w')
	notCalHandle = open("D:/programe-data/database/stockHistInfoDatabase/notCalGXLPB.log",'w')
	for item in uniqueStokeList1:
		tableName = "HistCal_" + item[0:6]
		if tableName in stockTableList:
			try:
				res = backTest(item[0:6]).onlyTestLatestTime()
				if res != 0:
					calResHandle.write(str(res) + " GXL is higher than 90% time! and higher than 3%! and PB is below 10%!\n")
			except Exception as e:
				print(tableName + " select error: " + str(e))
				notCalHandle.write(tableName + " select error: " + str(e) + "\n")
		else:
			notCalHandle.write(tableName + " not in calInfo.db\n")
				
				



		



			
