# Quick Fix for Database Error

## The Problem
The error `Table 'eventbooking_db.events_event' doesn't exist` means the database tables haven't been created yet.

## Solution (3 Steps)

### ⚠️ IMPORTANT: Stop the Server First!

**If you see the server running** (showing "Starting development server at http://127.0.0.1:8000/"), you **MUST stop it first**:

1. Go to the terminal/command prompt where the server is running
2. Press **`CTRL + C`** to stop it
3. Wait until you see the command prompt again (no server running)

### Then Run These Commands:

**Option 1: Use the batch file (Windows)**
```bash
run_migrations.bat
```

**Option 2: Run commands manually**
```bash
python manage.py makemigrations
python manage.py migrate
```

### After Migrations Complete:

Start the server again:
```bash
python manage.py runserver
```

## What These Commands Do:

1. **`makemigrations`** - Creates migration files based on your models
2. **`migrate`** - Creates the actual database tables in MySQL

## Expected Output:

After running `makemigrations`, you should see:
```
Migrations for 'events':
  events\migrations\0001_initial.py
    - Create model UserProfile
    - Create model EventCategory
    - Create model Event
    - Create model PhotographyPackage
    - Create model CateringPackage
    - Create model Booking
    - Create model BookingService
```

After running `migrate`, you should see:
```
Operations to perform:
  Apply all migrations: admin, auth, captcha, contenttypes, events, sessions
Running migrations:
  Applying events.0001_initial... OK
  ...
```

## If You Still Get Errors:

1. **Make sure MySQL is running**
2. **Check database exists:** Open MySQL and run `SHOW DATABASES;`
3. **Verify credentials** in `settings.py` match your MySQL setup

