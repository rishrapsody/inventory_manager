@echo off

echo Downloading Python installer...
curl -o python-installer.exe https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe

echo Installing Python...
python-installer.exe /quiet /passive TargetDir="%USERPROFILE%\AppData\Local\Programs\Python\Python38\"


REM Add Python and pip paths to environment variables
echo Updating environment variables...
setx PATH "%USERPROFILE%\AppData\Local\Programs\Python\Python38\;%USERPROFILE%\AppData\Local\Programs\Python\Python38\Scripts;%PATH%"
setx PYTHONPATH "%USERPROFILE%\AppData\Local\Programs\Python\Python38\;%USERPROFILE%\AppData\Local\Programs\Python\Python38\Lib;%PYTHONPATH%"

REM Install required Python packages using pip
echo Installing required packages...
echo Installing pandas...
python -m pip install pandas

echo Installing streamlit...
python -m pip install streamlit

echo Installing sqlite3...
python -m pip install sqlite3

echo Installing barcode...
python -m pip install barcode 

echo Installing python-barcode...
python -m pip install python-barcode 

echo Installing prettytable...
python -m pip install prettytable 

echo Done!
