@echo off
cd /d "d:\PMC\sims_project"
echo Starting Django development server...
py manage.py runserver 127.0.0.1:8000
pause
