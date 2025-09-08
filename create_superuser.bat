@echo off
echo 👤 Creating Superuser Account...
echo.
venv\Scripts\python manage.py createsuperuser
pause