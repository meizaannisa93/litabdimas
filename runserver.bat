@echo off
REM Jalankan server Django di jendela baru
start "" "C:\Users\abyre\.conda\envs\proyek1\python.exe" D:\proyeklatsar\litabdimas_project\manage.py runserver

REM Tunggu sebentar lalu buka browser
timeout /t 3 >nul
start "" http://127.0.0.1:8000

pause