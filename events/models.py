from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=20, choices=[
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin')
    ], default='user')
    is_active = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('concert', 'Concert'),
        ('festival', 'Festival'),
        ('exhibition', 'Exhibition'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    video = models.FileField(upload_to='events/videos/', null=True, blank=True)
    registration_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()


class PhotographyPackage(models.Model):
    PHOTO_TYPES = [
        ('candid', 'Candid'),
        ('traditional', 'Traditional'),
        ('both', 'Both'),
    ]

    DURATION_CHOICES = [
        ('2hrs', '2 Hours'),
        ('4hrs', '4 Hours'),
        ('full', 'Full Event'),
    ]

    DELIVERY_CHOICES = [
        ('drive', 'Google Drive'),
        ('pendrive', 'Pendrive'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    photo_count = models.CharField(max_length=50)  # "50", "150", "unlimited"
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    photographers_count = models.IntegerField(default=1)
    includes_editing = models.BooleanField(default=False)
    includes_album = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CateringPackage(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snacks', 'Snacks'),
    ]

    MENU_TYPES = [
        ('standard', 'Standard Menu'),
        ('custom', 'Custom Menu'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    price_per_plate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    supports_veg = models.BooleanField(default=True)
    supports_nonveg = models.BooleanField(default=False)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES, default='standard')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_meal_type_display()}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    event_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    attendance_marked = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"


class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(max_length=20, choices=[
        ('photography', 'Photography'),
        ('catering', 'Catering'),
    ])
    
    # Photography fields
    photography_package = models.ForeignKey(PhotographyPackage, on_delete=models.SET_NULL, null=True, blank=True)
    photo_type = models.CharField(max_length=20, choices=PhotographyPackage.PHOTO_TYPES, blank=True)
    duration = models.CharField(max_length=20, choices=PhotographyPackage.DURATION_CHOICES, blank=True)
    delivery_method = models.CharField(max_length=20, choices=PhotographyPackage.DELIVERY_CHOICES, blank=True)
    
    # Catering fields
    catering_package = models.ForeignKey(CateringPackage, on_delete=models.SET_NULL, null=True, blank=True)
    food_type = models.CharField(max_length=20, choices=[
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
        ('both', 'Both'),
    ], blank=True)
    plate_count = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    service_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.booking} - {self.service_type}"

