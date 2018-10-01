#calculate PE and PB from input list
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
from stock.dataSourceParse import getStockCodeList
from stock.back_test import backTest

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


calculationDatabase='D:/programe-data/database/stockHistInfoDatabase/calInfo.db'
stockCodeList = getStockCodeList().getListofStockCode()
uniqueStokeList1 = list(set(stockCodeList))
stockTableList = tableNameList(calculationDatabase)	
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