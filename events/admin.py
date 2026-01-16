from django.contrib import admin
from .models import (
    UserProfile, EventCategory, Event, PhotographyPackage,
    CateringPackage, Booking, BookingService
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_type', 'date', 'location', 'registration_enabled']
    list_filter = ['category', 'event_type', 'registration_enabled', 'date']
    search_fields = ['title', 'description', 'location', 'organizer']


@admin.register(PhotographyPackage)
class PhotographyPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_count', 'price', 'photographers_count', 'is_active']
    list_filter = ['is_active']


@admin.register(CateringPackage)
class CateringPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal_type', 'price_per_plate', 'menu_type', 'is_active']
    list_filter = ['meal_type', 'menu_type', 'is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'total_amount', 'booking_date', 'attendance_marked']
    list_filter = ['status', 'booking_date', 'attendance_marked']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['booking_date']


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ['booking', 'service_type', 'service_price']
    list_filter = ['service_type']

