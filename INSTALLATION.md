# Installation Guide - Django Event Booking Platform

## Quick Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note for Windows users:** If `mysqlclient` installation fails, you can:
- Install MySQL Connector/C from MySQL website, OR
- Use PyMySQL instead (see alternative below)

**Alternative: Using PyMySQL (Windows-friendly)**
1. Install PyMySQL: `pip install pymysql`
2. Add to `eventbooking/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 2. Set Up MySQL Database

1. **Start MySQL Server**

2. **Create Database:**
```sql
CREATE DATABASE eventbooking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Create .env file:**
   - Copy `.env.example` to `.env`
   - Update database credentials:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=eventbooking_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

4. **Generate Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and paste it in `.env` file as `SECRET_KEY`.

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### 5. Set Admin Role
```bash
python manage.py setup_admin your-admin-username
```
Replace `your-admin-username` with the username you created in step 4.

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Server
```bash
python manage.py runserver
```

## Access the Application

- **User Side:** http://127.0.0.1:8000/
- **Admin Dashboard:** http://127.0.0.1:8000/admin/dashboard/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Initial Setup

### Create Sample Data

1. **Login to Admin Dashboard** (http://127.0.0.1:8000/admin/dashboard/)

2. **Create Event Categories:**
   - Go to Django Admin → Event Categories
   - Add categories (e.g., "Technology", "Business", "Entertainment")

3. **Create Events:**
   - Go to Admin Dashboard → Events → Create Event
   - Fill in event details

4. **Create Photography Packages:**
   - Go to Admin Dashboard → Services
   - Click "Add Photography Package"
   - Create packages:
     - Basic: 50 photos, $100
     - Standard: 150 photos + editing, $250
     - Premium: Unlimited + 2 photographers + album, $500

5. **Create Catering Packages:**
   - Go to Admin Dashboard → Services
   - Click "Add Catering Package"
   - Create packages for different meal types (breakfast, lunch, dinner, snacks)

## Troubleshooting

### MySQL Connection Error
- Verify MySQL server is running
- Check database credentials in `.env`
- Ensure database exists: `SHOW DATABASES;`
- Grant permissions: `GRANT ALL PRIVILEGES ON eventbooking_db.* TO 'root'@'localhost';`

### Module Not Found Error
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check `DEBUG=True` in `.env` for development

### CAPTCHA Not Working
- Run migrations: `python manage.py migrate`
- Check `captcha` is in `INSTALLED_APPS` in settings.py

## Production Deployment

For production:
1. Set `DEBUG=False` in `.env`
2. Set proper `ALLOWED_HOSTS` in settings.py
3. Use a production WSGI server (e.g., Gunicorn)
4. Use a production database (configure connection pooling)
5. Set up proper static file serving (e.g., Nginx)
6. Use HTTPS
7. Set strong `SECRET_KEY`
8. Configure proper security headers

