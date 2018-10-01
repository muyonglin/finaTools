REM echo 'hello'
set ipython=D:\Anaconda3\Scripts\ipython.exe

start cmd /k %ipython% test.py && PAUSE

set test=%cd%
echo %test%
cd D:\Desktop\
start cmd /k %ipython% test.py && PAUSE

cd %test%
echo %cd%