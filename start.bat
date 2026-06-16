@echo off
start "Backend" /D "D:\reasonix.all\reasonnix-demo-one\home\user\projects\image-editor" .venv\Scripts\python manage.py runserver
start "Frontend" /D "D:\reasonix.all\reasonnix-demo-one\home\user\projects\furniture-factory" npm run dev
echo http://localhost:5173
echo http://127.0.0.1:8000/admin
pause
