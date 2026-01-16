# How to Run Migrations - Step by Step

## ⚠️ Important: Stop the Server First!

If your Django server is running (you see "Starting development server at http://127.0.0.1:8000/"), you need to **stop it first**:

1. Go to the terminal where the server is running
2. Press `CTRL + C` (or `CTRL + BREAK` on Windows) to stop the server

## Then Run These Commands:

### Step 1: Create Migration Files
```bash
python manage.py makemigrations
```

This should output something like:
```
Migrations for 'events':
  events\migrations\0001_initial.py
    - Create model UserProfile
    - Create model EventCategory
    - Create model Event
    ...
```

### Step 2: Apply Migrations to Database
```bash
python manage.py migrate
```

This will create all the tables in your MySQL database.

### Step 3: Start the Server Again
```bash
python manage.py runserver
```

Now the application should work without errors!

## If You Still Get Errors:

1. **Make sure MySQL is running**
2. **Verify database exists:**
   - Open MySQL command line
   - Run: `SHOW DATABASES;`
   - You should see `eventbooking_db` in the list

3. **Check database credentials** in `settings.py` match your MySQL setup

