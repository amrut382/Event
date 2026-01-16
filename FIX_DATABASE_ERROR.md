# Fix Database Error - Step by Step Guide

## ✅ Issue Fixed: CAPTCHA Warning
The CAPTCHA warning has been silenced in `settings.py`. This won't affect functionality.

## 🔧 Fix: Create MySQL Database

You need to create the database `eventbooking_db` in MySQL. Here are **3 easy methods**:

### Method 1: MySQL Command Line (Easiest)

1. **Open MySQL Command Line Client** or MySQL terminal
2. **Login** with your MySQL root password
3. **Run this command:**
   ```sql
   CREATE DATABASE eventbooking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
4. **Verify** it was created:
   ```sql
   SHOW DATABASES;
   ```
   You should see `eventbooking_db` in the list.

### Method 2: MySQL Workbench (GUI)

1. Open **MySQL Workbench**
2. Connect to your MySQL server
3. Click on **"Create a new schema"** (or right-click in Schemas panel)
4. Name it: `eventbooking_db`
5. Set **Charset/Collation** to: `utf8mb4` / `utf8mb4_unicode_ci`
6. Click **Apply**

### Method 3: Using Python Script (Alternative)

If you have `mysql-connector-python` installed:

1. **Update the password** in `create_db.py` (line 11) to match your MySQL password
2. **Run:**
   ```bash
   python create_db.py
   ```

Or install mysql-connector-python first:
```bash
pip install mysql-connector-python
```

## ✅ After Creating Database

Once the database is created, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This should work without errors!

## 🔍 Verify Database Connection

If you still get connection errors, check:

1. **MySQL is running:**
   - Windows: Check Services → MySQL
   - Or try: `mysql -u root -p`

2. **Password is correct:**
   - Check `eventbooking/settings.py` line 80
   - Or create a `.env` file with your credentials

3. **Database name matches:**
   - Should be: `eventbooking_db`
   - Or update in settings.py if you used a different name

## 📝 Quick Reference

**Current Database Settings** (in `settings.py`):
- Database: `eventbooking_db`
- User: `root`
- Password: `newpassword` (update if different)
- Host: `localhost`
- Port: `3306`

**To use a different database name/password:**
1. Create `.env` file in project root
2. Add:
   ```
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

