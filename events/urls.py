from django.urls import path
from . import views

urlpatterns = [
    # User side
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('booking/<int:event_id>/step1/', views.booking_step1, name='booking_step1'),
    path('booking/<int:booking_id>/step2/', views.booking_step2, name='booking_step2'),
    path('booking/<int:booking_id>/step3/', views.booking_step3, name='booking_step3'),
    path('booking/<int:booking_id>/confirm/', views.booking_confirm, name='booking_confirm'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Admin side
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/events/create/', views.admin_event_create, name='admin_event_create'),
    path('admin/events/<int:event_id>/edit/', views.admin_event_edit, name='admin_event_edit'),
    path('admin/events/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/<int:booking_id>/update-status/', views.admin_booking_update_status, name='admin_booking_update_status'),
    path('admin/bookings/<int:booking_id>/mark-attendance/', views.admin_booking_mark_attendance, name='admin_booking_mark_attendance'),
    path('admin/bookings/export/excel/', views.admin_booking_export_excel, name='admin_booking_export_excel'),
    path('admin/bookings/export/pdf/', views.admin_booking_export_pdf, name='admin_booking_export_pdf'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('admin/users/<int:user_id>/bookings/', views.admin_user_bookings, name='admin_user_bookings'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/services/photography/create/', views.admin_photography_create, name='admin_photography_create'),
    path('admin/services/catering/create/', views.admin_catering_create, name='admin_catering_create'),
]

