#calculate PE and PB from input list
import sys
sys.path.append("D:/codes/stocks/infomationTools")  
from parentObject import generalFunction

class calculatePEPB(generalFunction):
	"""@input: stock code, stock exchange, 
	   		   startDate ('yyyy-mm-dd'), stopDate ('yyyy-mm-dd')
	   		   data source (yahoo for price and dongFangCaiFu for financial) 
	   @methods: add ,, to price Dataframe
	   			 calculate PE,PB and add it to the DataFrame
	   @output:	   
	"""
	def __init__(self, stockCode,priceDatabasePath="D:/programe-data/database/stockHistInfoDatabase/stockInfo.db",finaDatabase="D:/programe-data/database/stockHistInfoDatabase/stockFinanInfo.db"):

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
			priceData = generalFunction.fetchDataFromDatabase(self,self.dPp,tableNameH_t,['date','close'])		
		elif tableNameH_y in tableNameList:
			priceData = generalFunction.fetchDataFromDatabase(self,self.dPp,tableNameH_y,['date','close'])		
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
		#mgjscData
		#[('date','tanBojzc'),(),()]	
		return(mgjzcData)	

	def getDividenData(self):
		tableNameD = "MeiNianFenHong_" + self.sc
		try:
			dividenData = generalFunction.fetchDataFromDatabase(self,self.dPf,tableNameD,['date','pai','song','zhuan'])
		except:
			dividenData = 0
			#print("can't fetch diveden data")
		return(dividenData) 
		
	def calculatePB(self):
		import datetime as dt
		#use list.sort() to make sure the order of date
		#priceData time, from oldest to today
		priceData = self.getPriceData()
		priceData.sort(key=lambda tup: tup[0])
		#print(priceData[0:50])
		#mgjzc time, from newest to oldest
		mgjzc = self.getMgjzcData()
		mgjzc.sort(key=lambda tup: tup[0],reverse=True)
		#print(mgjzc)
		#dividen time, from oldest to newest
		dividen = self.getDividenData()
		dividen.sort(key=lambda tup: tup[0])
		#print(dividen)
		mgjzcM = []
		tmpMgjzc = 0
		#将除权信息加入净资产计算
		if self.st(dividen[-1][0]) > self.st(mgjzc[0][0]):
			tmpMgjzc = round(((10 * float(mgjzc[0][1])) - float(dividen[-1][1]['派']))/(10 + float(dividen[-1][1]['送']) + float(dividen[-1][1]['转'])),4)
			mgjzcM.append((dividen[-1][0],tmpMgjzc))
		tmpMgjzc = 0	
		for i in range(len(mgjzc)-1):
			mgjzcM.append(mgjzc[i]) 
			for j in range(len(dividen)):
				if self.st(dividen[j][0]) < self.st(mgjzc[i][0]) and self.st(dividen[j][0]) > self.st(mgjzc[i+1][0]):
					tmpMgjzc = round(((10 * float(mgjzc[i+1][1])) - float(dividen[j][1]['派']))/(10 + float(dividen[j][1]['送']) + float(dividen[j][1]['转'])),4)
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
				PBList.append((priceData[i][0],tmpPB))
				continue
			else:	
				for j in range(len(mgjzcM)-1):
					if self.st(mgjzcM[j][0]) < self.st(priceData[0][0]):
						continue
					z = 0
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
	

	def calculateGuXiLv(self):
		import datetime as dt
		#use list.sort() to make sure the order of date is from oldest to newest
		#priceData time, from oldest to today
		priceData = self.getPriceData()
		priceData.sort(key=lambda tup: tup[0])
		#print(priceData[0:50])
		#dividen time, from oldest to newest
		#考虑每年分两次红的情况
		#[(date,pai,song,zhuan),(),()]
		dividen = self.getDividenData()
		if dividen != 0:
			#list.sort() to make sure the order of date is from oldest to newest
			dividen.sort(key=lambda tup: tup[0])
			#print(dividen)
			#guxilv = pai / (10 + song + zhuan) 
			tmpgxl = [] #[(date,guxilv,gx/10gu,price)]
			for i in xrange(len(priceData)):
				if self.st(priceData[i][0]) <= self.st(dividen[0][0]):
					tmpgxl.append((priceData[i][0],0,0,priceData[i][1]))
				else:
					for j in xrange(len(dividen)-1):
						pass

				pass

		pass

	def calculatePE(self):
		pass	
#选取市净率低的股票
def selectLowPBStock(yearRange='NA'):
	import pandas as pd
	from dataSourceParse import getStockCodeList
	outHandle1 = open("notCal.txt",'w')
	outHandle2 = open("lowPB.txt",'w')
	stockList = getStockCodeList().getListofStockCode()
	for item in stockList:
		try:
			PB = calculatePEPB(item[0:6]).calculatePB()
		except:
			outHandle1.write("can't calculate PB " + item[0:6])

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
			outHandle2.write(item[0:6] + " PB is below 10%!")

#选取股息率高的股票 
def selectHighGxlStock():
	pass			
	