@echo off

REM Set Python version
set PYTHON_VERSION=3.11.0

REM Set the virtual environment name
set VENV_NAME=myenv

REM Set the log file name
set LOG_FILE=install_log.txt


REM Create and activate the virtual environment
echo Creating virtual environment...
python -m venv %VENV_NAME%
call %VENV_NAME%\Scripts\activate.bat

REM Install required Python packages using pip
echo Installing required packages...

echo Installing pandas...
python -m pip install pandas >> %LOG_FILE%

echo Installing wheel...
python -m pip install wheel >> %LOG_FILE%

echo Installing streamlit...
python -m pip install streamlit >> %LOG_FILE%

echo Installing sqlite3...
python -m pip install sqlite3 >> %LOG_FILE%

echo Installing barcode...
python -m pip install barcode >> %LOG_FILE%

echo Installing python-barcode...
python -m pip install python-barcode >> %LOG_FILE%

echo Installing prettytable...
python -m pip install prettytable >> %LOG_FILE%

echo Done!
