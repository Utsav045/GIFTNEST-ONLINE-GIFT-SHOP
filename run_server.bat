@echo off
echo 🚀 Starting GiftNest Server...
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.
venv\Scripts\python manage.py runserver
pause