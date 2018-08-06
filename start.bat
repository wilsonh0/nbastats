call env\Scripts\Activate.bat
@echo on
set env=env\Scripts\python.exe
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
@echo off
pause