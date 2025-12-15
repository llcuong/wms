@echo off
call .venv\Scripts\activate
cd backend
python manage.py runserver 0.0.0.0:30000
pause