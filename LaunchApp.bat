@echo off

REM Set the path to the Streamlit script
set STREAMLIT_SCRIPT=streamlitcode.py

REM Set the virtual environment name
set VENV_NAME=myenv

REM Set the log file name
set LOG_FILE=streamlit_log.txt

REM Launch command prompt and execute Streamlit command
start cmd /k "call %VENV_NAME%\Scripts\activate.bat && streamlit run %STREAMLIT_SCRIPT% 2>&1"
