@echo off
echo ========================================
echo Running Django Migrations
echo ========================================
echo.
echo Step 1: Creating migration files...
python manage.py makemigrations
echo.
echo Step 2: Applying migrations to database...
python manage.py migrate
echo.
echo ========================================
echo Migrations completed!
echo ========================================
echo.
echo You can now start the server with: python manage.py runserver
pause

