import sys
sys.path.append("D:/codes/stocks/infomationTools/stock")  
from calculation import calculatePEPB, selectLowPBStock

#calculatePEPB('000876').plotHistoricalPB(10)
#a = calculatePEPB('000876').calculatePB()
#select stock 
#import os
#os.chdir("D:/desktop")
#selectLowPBStock()




…or create a new repository on the command line
 echo "# finaTools" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/muyonglin/finaTools.git
git push -u origin master
…or push an existing repository from the command line
 git remote add origin https://github.com/muyonglin/finaTools.git
git push -u origin master
…or import code from another repository
You can initialize this repository with code from a Subversion, Mercurial, or TFS project.




#dataSourceParse.py
download price, finacial and stock list data from website
write these data into sqlite3 database

#databaseMaintainance.py
updata downloaded or calculated data into database