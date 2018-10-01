REM echo 'hello'
set ipython=D:\Anaconda3\Scripts\ipython.exe
start cmd /c %ipython% stockPriceUpdate.py
SLEEP 60
%ipython% xueQiuFinanUpdate.py &&  %ipython% calculateDatabase.py 

echo database updates done
PAUSE