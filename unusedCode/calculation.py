#calculate PE and PB from input list
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction
#from stock.calculation import calculatePEPB
from stock.dataSourceParse import getStockCodeList
from stock.back_test import backTest

class calculatePEPB(generalFunction):
	"""@input: stock code, stock exchange, 
	   		   startDate ('yyyy-mm-dd'), stopDate ('yyyy-mm-dd')
	   		   data source (yahoo for price and dongFangCaiFu for financial) 
	   @methods: add ,, to price Dataframe
	   			 calculate PE,PB and add it to the DataFrame
	   @output:	   
	"""
	def __init__(self, stockCode
		,priceDatabasePath="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db"
		,finaDatabase="D:/programe-data/database/stockHistInfoDatabase/stockFinanInfo.db"):

		self.sc = stockCode
		self.dPp = priceDatabasePath
		self.dPf = finaDatabase
		# self.price = self.getPriceData()
		# self.mgsy = self.getMgsyData()
		# self.mgjzc = self.getMgjzcData()
		# self.dividen = getDividenData()
		#self.convertPriceAndFinan()

	#计算 普通股每年每股盈利 (动态盈利，静态盈利)
	#计算 盈利增长比率
	#计算 每股净资产
	def st(self,timeString):
		import datetime as dt
		#timeString in "%Y-%m-%d" format
		return(dt.datetime.strptime(timeString,'%Y-%m-%d'))

		
	def getPriceData(self):
		tableNameH_y = "HistPrice_" + self.sc
		tableNameH_t = "HistPrice_" + self.sc + "_tencent"
		tableNameList = generalFunction.tableNameList(self)
		if tableNameH_t in tableNameList:
			try:
				priceData = generalFunction.fetchDataFromDatabase(self,self.dPp,tableNameH_t,['date','close'])		
			except:
				print("can't fetch tencent price data")	
				priceData = 0
		elif tableNameH_y in tableNameList:
			try:
				priceData = generalFunction.fetchDataFromDatabase(self,self.dPp,tableNameH_y,['date','close'])		
			except:
				print("can't fetch yahoo price data")	
				priceData = 0				
				
		#priceData
		#[(date,close),(),()]
		return(priceData)
	def getMgsyData(self):
		tableNameMS = "MeiGuShouYi_" + self.sc
		try:
			mgsyData = generalFunction.fetchDataFromDatabase(self,self.dPf,tableNameMS,['date','nianMoZuiXintbst','gunDongtbsy'])
		except:
			print("can't fetch Mgsy data")
		#mgsyData
		#[('date','nianMoZuiXintbst','gunDongtbsy'),(),()]	
		return(mgsyData)	

	def getMgjzcData(self):
		tableNameMZ = "MeiGuJingZiChan_" + self.sc
		try:
			mgjzcData = generalFunction.fetchDataFromDatabase(self,self.dPf,tableNameMZ,['date','tanBojzc'])
		except:
			print("can't fetch mgjzc data")
			mgjzcData = 0
		#mgjscData
		#[('date','tanBojzc'),(),()]	
		return(mgjzcData)	

	def getDividenData(self):
		tableNameD = "MeiNianFenHong_" + self.sc
		try:
			dividenData = generalFunction.fetchDataFromDatabase(self,self.dPf,tableNameD,['date','pai','song','zhuan'])
		except:
			dividenData = 0
			print("can't fetch diveden data")
		return(dividenData)

	def getDividenDataFromTencent(self):
		import datetime as dt
		tableNameD = "Dividend_" + self.sc + "_tencent"
		try:
			#cqr 分红已发放，股价降低， djr 股价未变化
			dividenData = generalFunction.fetchDataFromDatabase(self,self.dPp,tableNameD,['date','FHcontent','cqr','djr'])
			tmpList = [] #[('cqr',pai,song,zhuan),(),()]
			for item in dividenData:
				fhDict = generalFunction.splitDivString(self,item[1])
				tmpList.append((item[2],fhDict['派'],fhDict['送'],fhDict['转']))
			dividenData = tmpList	
			dividenData.sort(key=lambda tup: tup[0])
			tmpDL = dividenData.copy()
			z = 0
			for i in range(len(dividenData) - 1):
				#print(dividenData[i])
				if (int(dividenData[i+1][0][0:4]) - int(dividenData[i][0][0:4])) > 1:
					for j in range(1,(int(dividenData[i+1][0][0:4]) - int(dividenData[i][0][0:4]))):
						tmpDL.insert(i+z+j,
							(str(int(dividenData[i][0][0:4])+j) + dividenData[i][0][4:],0,0,0))
					z += (int(dividenData[i+1][0][0:4]) - int(dividenData[i][0][0:4])) - 1
			dividenData = tmpDL	
		except Exception as e:
			print(e)
			dividenData = 0
		return(dividenData)			  
		
	def calculatePB(self):
		import datetime as dt
		#use list.sort() to make sure the order of date
		#priceData time, from oldest to today
		priceData = self.getPriceData()
		priceData.sort(key=lambda tup: tup[0])
		#print(priceData[0])
		#print(priceData[0:50])
		#mgjzc time, from newest to oldest
		mgjzc = self.getMgjzcData()
		mgjzc.sort(key=lambda tup: tup[0],reverse=True)
		#print(mgjzc)
		#dividen time, from oldest to newest
		#dividen = self.getDividenData()
		#[('cqr',pai,song,zhuan),(),()]
		dividen = self.getDividenDataFromTencent()
		dividen.sort(key=lambda tup: tup[0])
		#print(dividen)
		if priceData == 0 or mgjzc ==0:
			return(0)
		else:	
			#将 '--' 替换为前一季度的 mgjzc
			for i in range(2,len(mgjzc)+1):
				if mgjzc[-i][1] != '--' and mgjzc[-i][1] != '0':
					continue
				elif mgjzc[-i][1] == '0':
					mgjzc[-i] = (mgjzc[-i][0],'0.01') 
				elif mgjzc[-i][1] == '--':
					mgjzc[-i] = (mgjzc[-i][0],mgjzc[-i+1][1]) 
			#print(mgjzc)	
			#将除权信息加入净资产计算
			if len(dividen) == 0:
				mgjzcM = mgjzc
			else:	
				mgjzcM = []
				tmpMgjzc = 0
				if self.st(dividen[-1][0]) > self.st(mgjzc[0][0]):
					tmpMgjzc = round(((10 * float(mgjzc[0][1])) - float(dividen[-1][1]))/(10 + float(dividen[-1][2]) + float(dividen[-1][3])),4)
					mgjzcM.append((dividen[-1][0],tmpMgjzc))
				tmpMgjzc = 0	
				for i in range(len(mgjzc)-1):
					mgjzcM.append(mgjzc[i]) 
					for j in range(len(dividen)):
						if self.st(dividen[j][0]) < self.st(mgjzc[i][0]) and self.st(dividen[j][0]) > self.st(mgjzc[i+1][0]):
							tmpMgjzc = round(((10 * float(mgjzc[i+1][1])) - float(dividen[j][1]))/(10 + float(dividen[j][2]) + float(dividen[j][3])),4)
							mgjzcM.append((dividen[j][0],tmpMgjzc))
			#print(mgjzcM)
			#mgjzcM time, from newest to oldest
			#reversed mgjacM time, from oldest to newest
			mgjzcM.reverse()
			#print(mgjzcM)
			#print(priceData)
			PBList = []
			for i in range(len(priceData)):
				if self.st(priceData[i][0]) > self.st(mgjzcM[-1][0]):
					#print(priceData[i][0])
					#print((priceData[i][0],tmpPB))
					tmpPB =round(float(priceData[i][1])/float(mgjzcM[-1][1]),4)
					#print(priceData[i],mgjzcM[-1],tmpPB)
					PBList.append((priceData[i][0],tmpPB))
					continue
				else:	
					for j in range(len(mgjzcM)-1):
						z = 0
						if self.st(mgjzcM[j][0]) < self.st(priceData[0][0]):
							continue					
						if self.st(priceData[i][0])	>= self.st(mgjzcM[j][0]) and self.st(priceData[i][0]) < self.st(mgjzcM[j+1][0]):
							#print(mgjzcM[j][1])
							tmpPB = round((float(priceData[i][1])/float(mgjzcM[j][1])),4)	
							#print((priceData[i][0],tmpPB))
							z = 1
							PBList.append((priceData[i][0],tmpPB))
							break
					if z == 0:
						pass
						#print(priceData[i][0] + " not calculated")
			return(PBList)
	def plotHistoricalPB(self,yearRange='NA'):
		PB = self.calculatePB()
		dataRange = 0
		if yearRange != 'NA':
			dataRange = yearRange * 280
		if len(PB) > dataRange:
			PB = PB[-dataRange:]	 
		import pandas as pd
		import matplotlib.pyplot as plt
		PBtmp = pd.DataFrame(PB)
		PBtmp.iloc[:,0] = pd.to_datetime(PBtmp.iloc[:,0])
		PBtmp.iloc[:,1] = pd.to_numeric(PBtmp.iloc[:,1])
		plt.plot(PBtmp.iloc[:,0],PBtmp.iloc[:,1])
		plt.axhline(PBtmp.iloc[:,1].quantile(0.9),color='red')
		plt.axhline(PBtmp.iloc[:,1].quantile(0.7),color='brown')		
		plt.axhline(PBtmp.iloc[:,1].quantile(0.3),color='blue')
		plt.axhline(PBtmp.iloc[:,1].quantile(0.1),color='green')
		plt.show()
		print("top 10 percent PB value:" + str(round(PBtmp.iloc[:,1].quantile(0.9),4)))
		print("top 30 percent PB value:" + str(round(PBtmp.iloc[:,1].quantile(0.7),4)))
		print("bottom 30 percent PB value:" + str(round(PBtmp.iloc[:,1].quantile(0.3),4)))
		print("bottom 10 percent PB value:" + str(round(PBtmp.iloc[:,1].quantile(0.1),4)))
		print('lwest PB value: ' + str(round(min(PBtmp.iloc[:,1]),4)))
		print('current PB value: ' + str(round(PBtmp.iloc[-1,1],4)))
	

	def calculateGuXiLv(self):
		import datetime as dt
		#use list.sort() to make sure the order of date is from oldest to newest
		#priceData time, from oldest to today
		priceData = self.getPriceData()
		priceData.sort(key=lambda tup: tup[0])
		#有些新股还没有价格数据（刚发行） 
		if priceData == []:
			return(0)
		#print(priceData[0:50])
		#dividen time, from oldest to newest
		#考虑每年分两次红的情况
		#使用 tencent 分红 Data，
		#[('date','FHcontent','cqr','djr'),(),()] -> [('cqr',pai,song,zhuan),(),()]
		dividen = self.getDividenDataFromTencent()
		#dividenWithSplitString [[(),{}],[(),{}]]	
		#[(date,pai,song,zhuan),(),()]
		#dividen = self.getDividenData()
		if dividen != 0:
			#list.sort() to make sure the order of date is from oldest to newest
			dividen.sort(key=lambda tup: tup[0])
			indexList = []
			dividen_m = []
			# print(len(dividen))
			# print(dividen)
			# print(dividen[16][0][:4])
			# print(list(range(len(dividen)-1)))
			for i in range(len(dividen) - 1):
				# print(dividen[i][0][0:4] )
				# print(i)
				# print(dividen[i+1][0][0:4])
				if dividen[i][0][0:4] == dividen[i+1][0][0:4]:
					dividen[i+1] = (dividen[i+1][0]
						,float(dividen[i][1]) + float(dividen[i+1][1])
						,float(dividen[i][2]) + float(dividen[i+1][2])
						,float(dividen[i][3]) + float(dividen[i+1][3]))
					indexList.append(i)
			# print(indexList)
			dividen_m = [i for j, i in enumerate(dividen) if j not in indexList]
			# print(dividen_m)
			dividen = dividen_m
			#print(dividen)
			#guxilv = (pai / (10 + song + zhuan))/price 
			tmpgxl = [] #[(date,guxilv,gx/10gu,price)]
			# print(len(dividen))
			# print(dividen)
			a = 0; b=0; c=0
			for i in range(len(priceData)):
				if self.st(priceData[i][0]) < self.st(dividen[0][0]):
					tmpgxl.append((priceData[i][0],0,0,priceData[i][1]))
				else:
					for j in range(len(dividen)-1):
						if self.st(priceData[i][0]) >= self.st(dividen[j][0]) and self.st(priceData[i][0]) < self.st(dividen[j+1][0]):
							tmpgxl.append((priceData[i][0]
								,(float(dividen[j][1])/(10 + float(dividen[j][2]) + float(dividen[j][3])))/float(priceData[i][1]) 
								,dividen[j][1] 
								,priceData[i][1]))		
					if self.st(priceData[i][0]) >= self.st(dividen[-1][0]) and (self.st(priceData[i][0]) - self.st(dividen[-1][0])) < dt.timedelta(400):
						tmpgxl.append((priceData[i][0]
							,(float(dividen[-1][1])/(10 + float(dividen[-1][2]) + float(dividen[-1][3])))/float(priceData[i][1]) 
							,dividen[-1][1] 
							,priceData[i][1]))
					elif (self.st(priceData[i][0]) - self.st(dividen[-1][0])) >= dt.timedelta(400):
						tmpgxl.append((priceData[i][0],0,0,priceData[i][1]))
			return(tmpgxl)
		else:
			return(0)
			
	def plotHistoricalGXL(self,yearRange='NA'):
		GXL = self.calculateGuXiLv()
		dataRange = 0
		if yearRange != 'NA':
			dataRange = yearRange * 280
		if len(GXL) > dataRange:
			GXL = GXL[-dataRange:]	 
		import pandas as pd
		import matplotlib.pyplot as plt
		GXLtmp = pd.DataFrame(GXL)
		GXLtmp.iloc[:,0] = pd.to_datetime(GXLtmp.iloc[:,0])
		GXLtmp.iloc[:,1] = pd.to_numeric(GXLtmp.iloc[:,1])
		plt.plot(GXLtmp.iloc[:,0],GXLtmp.iloc[:,1])
		plt.axhline(GXLtmp.iloc[:,1].quantile(0.9),color='red')
		plt.axhline(GXLtmp.iloc[:,1].quantile(0.7),color='brown')		
		plt.axhline(GXLtmp.iloc[:,1].quantile(0.3),color='blue')
		plt.axhline(GXLtmp.iloc[:,1].quantile(0.1),color='green')
		plt.show()
		print("top 10 percent GXL value:" + str(round(GXLtmp.iloc[:,1].quantile(0.9),4)))
		print("top 30 percent GXL value:" + str(round(GXLtmp.iloc[:,1].quantile(0.7),4)))
		print("bottom 30 percent GXL value:" + str(round(GXLtmp.iloc[:,1].quantile(0.3),4)))
		print("bottom 10 percent GXL value:" + str(round(GXLtmp.iloc[:,1].quantile(0.1),4)))
	
	def calculatePE(self):
		pass	
#选取市净率低的股票
def selectLowPBStock(yearRange='NA',stockCodeList = 'NA'):
	import pandas as pd
	from dataSourceParse import getStockCodeList
	outHandle1 = open("notCalPB.txt",'w')
	outHandle2 = open("lowPB.txt",'w')
	if stockCodeList == "NA":
		stockList = getStockCodeList().getListofStockCode()
	else:
		stockList = stockCodeList	
	for item in stockList:
		try:
			PB = calculatePEPB(item[0:6]).calculatePB()
		except:
			outHandle1.write("can't calculate PB " + item[0:6] + "\n")
			continue

		dataRange = 0
		if yearRange != 'NA':
			dataRange = yearRange * 280
		if len(PB) >= dataRange:
			PB = PB[-dataRange:]
		if 	len(PB) < dataRange:
			continue	
		PBtmp = pd.DataFrame(PB)
		PBtmp.iloc[:,0] = pd.to_datetime(PBtmp.iloc[:,0])
		PBtmp.iloc[:,1] = pd.to_numeric(PBtmp.iloc[:,1])
	

		if float(PB[-1][1]) < PBtmp.iloc[:,1].quantile(0.1):
			outHandle2.write(item[0:6] + " PB is below 10%!\n")
	outHandle1.close()
	outHandle2.close()		

#选取股息率高的股票 
def selectHighGxlStock(yearRange='NA'):
	import pandas as pd
	from dataSourceParse import getStockCodeList
	outHandle1 = open("notCalDiv.txt",'w')
	outHandle2 = open("HighDividen.txt",'w')
	stockList = getStockCodeList().getListofStockCode()
	HighDivList = []
	for item in stockList:
		try:
			#[(date,guxilv,gx/10gu,price)]
			GXL = calculatePEPB(item[0:6]).calculateGuXiLv()
		except Exception as e:
			outHandle1.write("can't calculate GXL " + item[0:6] + "\n")
			print(e)	
			continue	
		dataRange = 0
		#print(type(GXL))
		if type(GXL) != list:
			print(str(type(GXL)) + ' ' + str(item[0:6]))
			continue
		else:				
			if yearRange != 'NA':
				dataRange = yearRange * 280
			if len(GXL) >= dataRange:
				GXL = GXL[-dataRange:]
			if 	len(GXL) < dataRange:
				continue
			GXLtmp = pd.DataFrame(GXL)
			print(item[0:6])
			#GXLtmp.iloc[:,0] = 	pd.to_datetime(GXLtmp.iloc[:,0])
			GXLtmp.iloc[:,1] = pd.to_numeric(GXLtmp.iloc[:,1])
			if (GXLtmp.iloc[:,1] == 0).sum()/len(GXLtmp.iloc[:,1]) > 0.1:
				continue
			else:
				if float(GXL[-1][1]) > GXLtmp.iloc[:,1].quantile(0.9) and float(GXL[-1][1]) > 0.03:
					outHandle2.write(item[0:6] + " GXL is higher than 90% time! and higher than 3%!\n")
					#print(item[0:6] + " GXL is higher than 90%!\n")
					HighDivList.append(item)
	outHandle1.close()
	outHandle2.close()		
	return(HighDivList)


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
	import os
	os.chdir('D:/programe-data/database/stockHistInfoDatabase/selectionResults')
	selectLowPBStock('NA',selectHighGxlStock('NA'))

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
