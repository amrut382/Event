# Django Event Booking Platform

A comprehensive event booking system with add-on services (Photography and Catering) built with Django.

## Features

### User Side
- Browse events with search and filters (category, type, location)
- View event details with images and optional video clips
- User registration and login with security features
- Multi-step booking workflow:
  - Step 1: Event registration details
  - Step 2: Add-on services selection (Photography & Catering)
  - Step 3: Price summary
  - Step 4: Confirm booking
- View booking status (pending/confirmed/rejected/completed)
- Responsive footer with social links

### Admin Side
- Dashboard with KPIs (total events, bookings, users, upcoming events, recent registrations)
- Event Management (create/update/delete, enable/disable registrations)
- Booking Management (view, filter, approve/reject, mark attendance, export to Excel/PDF)
- User Management (view users, block/deactivate, view booking history)
- Service Management (manage photography and catering packages)
- Reports (monthly bookings chart, event-wise registrations, most popular events)

### Security Features
- CAPTCHA on login and registration
- Session timeout (30 minutes)
- Account lockout after 3 failed login attempts
- Role-based access control (Admin, Staff, User)

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd D:\vasanta
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient` on Windows, you can:
1. Install MySQL Connector/C from MySQL website
2. Or use `pip install mysqlclient` with pre-built wheels
3. Or use `pip install pymysql` and modify settings.py to use PyMySQL instead

### Step 4: Configure MySQL Database

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE eventbooking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Create .env file:**
   Copy `.env.example` to `.env` and update with your MySQL credentials:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=eventbooking_db
   DB_USER=root
   DB_PASSWORD=your-mysql-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. **Generate Secret Key:**
   You can generate a secret key using:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Create User Profile for Admin
After creating the superuser, you need to set the role to 'admin'. You can do this via Django admin panel or Python shell:

```python
python manage.py shell
```

```python
from django.contrib.auth.models import User
from events.models import UserProfile

user = User.objects.get(username='your-admin-username')
profile, created = UserProfile.objects.get_or_create(user=user)
profile.role = 'admin'
profile.phone = '1234567890'
profile.address = 'Admin Address'
profile.save()
```

### Step 8: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 9: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Accessing the Application

1. **User Side:** Navigate to `http://127.0.0.1:8000/`
   - Browse events
   - Register/Login
   - Book events with add-on services

2. **Admin Side:** Navigate to `http://127.0.0.1:8000/admin/dashboard/`
   - Login with admin credentials
   - Manage events, bookings, users, and services

### Creating Sample Data

You can create sample data through:
1. Django Admin Panel (`http://127.0.0.1:8000/admin/`)
2. Admin Dashboard (after logging in as admin)

### Setting Up Add-on Services

1. **Photography Packages:**
   - Go to Admin Dashboard → Services
   - Create photography packages (Basic, Standard, Premium)

2. **Catering Packages:**
   - Go to Admin Dashboard → Services
   - Create catering packages with meal types and pricing

## Project Structure

```
eventbooking/
├── eventbooking/          # Main project directory
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── events/               # Events app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Form classes
│   ├── urls.py           # App URL configuration
│   ├── admin.py          # Admin configuration
│   └── middleware.py     # Custom middleware
├── templates/            # HTML templates
│   ├── base.html
│   └── events/
│       ├── home.html
│       ├── event_detail.html
│       └── admin/
│           └── dashboard.html
├── static/               # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── media/                # User uploaded files
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md            # This file
```

## Database Models

- **UserProfile:** Extended user information with role and security settings
- **EventCategory:** Event categories
- **Event:** Event details with images and videos
- **PhotographyPackage:** Photography service packages
- **CateringPackage:** Catering service packages
- **Booking:** Event bookings
- **BookingService:** Add-on services linked to bookings

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Configure proper ALLOWED_HOSTS for production
- Use HTTPS in production
- Regularly update dependencies

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL server is running
- Verify database credentials in `.env`
- Check MySQL user has proper permissions
- Try using `pymysql` instead of `mysqlclient` if issues persist

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py
- Ensure `DEBUG=True` for development

### CAPTCHA Not Working
- Run migrations: `python manage.py migrate`
- Check `captcha` is in `INSTALLED_APPS`

## License

This project is open source and available for use.

## Support

For issues or questions, please check the Django documentation or create an issue in the project repository.

