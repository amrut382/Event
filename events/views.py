from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
import json
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import (
    Event, Booking, BookingService, PhotographyPackage, CateringPackage,
    UserProfile, EventCategory
)
from .forms import (
    UserRegistrationForm, LoginForm, EventSearchForm, BookingForm,
    PhotographyServiceForm, CateringServiceForm, EventForm,
    PhotographyPackageForm, CateringPackageForm
)
import json


def is_admin(user):
    try:
        return user.userprofile.role == 'admin'
    except:
        return False


def is_staff_or_admin(user):
    try:
        return user.userprofile.role in ['admin', 'staff']
    except:
        return False


# User Side Views
def home(request):
    # Show all events on home page (filter can be applied via search)
    events = Event.objects.all()
    form = EventSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        event_type = form.cleaned_data.get('event_type')
        location = form.cleaned_data.get('location')
        
        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category:
            events = events.filter(category=category)
        if event_type:
            events = events.filter(event_type=event_type)
        if location:
            events = events.filter(location__icontains=location)
    
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = EventCategory.objects.all()
    
    return render(request, 'events/home.html', {
        'page_obj': page_obj,
        'form': form,
        'categories': categories,
        'request': request,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Preserve next parameter if exists for redirect after login/register
    next_url = request.GET.get('next', None)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'next_url': next_url,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    next_url = request.GET.get('next', 'home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Event Booking Platform.')
            
            # Redirect to booking page if 'next' parameter exists
            if next_url and next_url != 'home':
                return redirect(next_url)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'events/register.html', {'form': form, 'next_url': next_url})


def user_login(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'home')
        return redirect(next_url)
    
    next_url = request.GET.get('next', 'home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(username=username)
                profile = user.userprofile
                
                # Check if account is locked
                if profile.locked_until and profile.locked_until > timezone.now():
                    messages.error(request, f'Account is locked. Try again after {profile.locked_until.strftime("%H:%M:%S")}')
                    return render(request, 'events/login.html', {'form': form, 'next_url': next_url})
                
                user = authenticate(request, username=username, password=password)
                if user:
                    profile.failed_login_attempts = 0
                    profile.locked_until = None
                    profile.save()
                    login(request, user)
                    # Redirect to next URL (booking page or event detail)
                    if next_url and next_url != 'home':
                        return redirect(next_url)
                    return redirect('home')
                else:
                    profile.failed_login_attempts += 1
                    if profile.failed_login_attempts >= 3:
                        profile.locked_until = timezone.now() + timedelta(minutes=5)
                        messages.error(request, 'Account locked for 5 minutes due to multiple failed attempts.')
                    else:
                        messages.error(request, f'Invalid credentials. {3 - profile.failed_login_attempts} attempts remaining.')
                    profile.save()
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    
    return render(request, 'events/login.html', {'form': form, 'next_url': next_url})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def booking_step1(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if not event.registration_enabled:
        messages.error(request, 'Registration for this event is currently disabled.')
        return redirect('event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                event_fee=event.price,
                total_amount=event.price,
                notes=form.cleaned_data['notes']
            )
            return redirect('booking_step2', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'events/booking_step1.html', {'event': event, 'form': form})


@login_required
def booking_step2(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        # Clear existing services
        BookingService.objects.filter(booking=booking).delete()
        total_addon = 0
        
        # Handle Photography
        photography_package_id = request.POST.get('photography_package')
        if photography_package_id:
            try:
                package = PhotographyPackage.objects.get(id=photography_package_id, is_active=True)
                service = BookingService.objects.create(
                    booking=booking,
                    service_type='photography',
                    photography_package=package,
                    photo_type=request.POST.get('photo_type', ''),
                    duration=request.POST.get('duration', ''),
                    delivery_method=request.POST.get('delivery_method', ''),
                    service_price=package.price
                )
                total_addon += package.price
            except PhotographyPackage.DoesNotExist:
                pass
        
        # Handle Catering
        catering_package_id = request.POST.get('catering_package')
        plate_count = request.POST.get('plate_count')
        if catering_package_id and plate_count:
            try:
                package = CateringPackage.objects.get(id=catering_package_id, is_active=True)
                plate_count = int(plate_count)
                if plate_count > 0:
                    service = BookingService.objects.create(
                        booking=booking,
                        service_type='catering',
                        catering_package=package,
                        food_type=request.POST.get('food_type', ''),
                        plate_count=plate_count,
                        service_price=package.price_per_plate * plate_count
                    )
                    total_addon += package.price_per_plate * plate_count
            except (CateringPackage.DoesNotExist, ValueError):
                pass
        
        booking.total_amount = booking.event_fee + total_addon
        booking.save()
        
        return redirect('booking_step3', booking_id=booking.id)
    
    photography_form = PhotographyServiceForm()
    catering_form = CateringServiceForm()
    photography_packages = PhotographyPackage.objects.filter(is_active=True)
    catering_packages = CateringPackage.objects.filter(is_active=True)
    
    return render(request, 'events/booking_step2.html', {
        'booking': booking,
        'photography_form': photography_form,
        'catering_form': catering_form,
        'photography_packages': photography_packages,
        'catering_packages': catering_packages,
    })


@login_required
def booking_step3(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    services = booking.services.all()
    
    return render(request, 'events/booking_step3.html', {
        'booking': booking,
        'services': services,
    })


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'pending'
    booking.save()
    messages.success(request, 'Booking submitted successfully! Waiting for admin approval.')
    return redirect('my_bookings')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'events/my_bookings.html', {'bookings': bookings})


# Admin Side Views
@login_required
@user_passes_test(is_staff_or_admin)
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    upcoming_events = Event.objects.filter(date__gte=timezone.now().date()).count()
    recent_registrations = Booking.objects.filter(
        booking_date__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    # Monthly bookings data for chart
    monthly_bookings = Booking.objects.filter(
        booking_date__gte=timezone.now() - timedelta(days=30)
    ).values('booking_date__date').annotate(count=Count('id')).order_by('booking_date__date')
    
    # Event-wise registrations
    event_registrations = Event.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:10]
    
    context = {
        'total_events': total_events,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'upcoming_events': upcoming_events,
        'recent_registrations': recent_registrations,
        'monthly_bookings': mark_safe(json.dumps(list(monthly_bookings))),
        'event_registrations': event_registrations,
    }
    
    return render(request, 'events/admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_events(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/admin/events.html', {'events': events})


@login_required
@user_passes_test(is_admin)
def admin_event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('admin_events')
    else:
        form = EventForm()
    
    return render(request, 'events/admin/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
@user_passes_test(is_admin)
def admin_event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('admin_events')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/admin/event_form.html', {'form': form, 'title': 'Edit Event', 'event': event})


@login_required
@user_passes_test(is_admin)
def admin_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('admin_events')
    return render(request, 'events/admin/event_delete.html', {'event': event})


@login_required
@user_passes_test(is_staff_or_admin)
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    
    # Filters
    event_filter = request.GET.get('event')
    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')
    
    if event_filter:
        bookings = bookings.filter(event_id=event_filter)
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if date_filter:
        bookings = bookings.filter(booking_date__date=date_filter)
    
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    events = Event.objects.all()
    
    return render(request, 'events/admin/bookings.html', {
        'page_obj': page_obj,
        'events': events,
        'status_filter': status_filter,
        'event_filter': event_filter,
        'date_filter': date_filter,
    })


@login_required
@user_passes_test(is_staff_or_admin)
def admin_booking_update_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Booking.STATUS_CHOICES):
            booking.status = status
            booking.save()
            messages.success(request, f'Booking status updated to {status}.')
    return redirect('admin_bookings')


@login_required
@user_passes_test(is_staff_or_admin)
def admin_booking_mark_attendance(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.attendance_marked = True
    booking.save()
    messages.success(request, 'Attendance marked successfully!')
    return redirect('admin_bookings')


@login_required
@user_passes_test(is_staff_or_admin)
def admin_booking_export_excel(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Bookings"
    
    # Headers
    ws.append(['User', 'Event', 'Status', 'Event Fee', 'Total Amount', 'Booking Date', 'Attendance'])
    
    # Data
    for booking in bookings:
        ws.append([
            booking.user.username,
            booking.event.title,
            booking.status,
            float(booking.event_fee),
            float(booking.total_amount),
            booking.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Yes' if booking.attendance_marked else 'No'
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bookings.xlsx'
    wb.save(response)
    return response


@login_required
@user_passes_test(is_staff_or_admin)
def admin_booking_export_pdf(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=bookings.pdf'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("Bookings Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Table data
    data = [['User', 'Event', 'Status', 'Total Amount', 'Date']]
    for booking in bookings:
        data.append([
            booking.user.username,
            booking.event.title,
            booking.status,
            str(booking.total_amount),
            booking.booking_date.strftime('%Y-%m-%d')
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'events/admin/users.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def admin_user_toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.userprofile
        profile.is_active = not profile.is_active
        profile.save()
        messages.success(request, f'User {"activated" if profile.is_active else "deactivated"} successfully!')
    except:
        messages.error(request, 'User profile not found.')
    return redirect('admin_users')


@login_required
@user_passes_test(is_admin)
def admin_user_bookings(request, user_id):
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    return render(request, 'events/admin/user_bookings.html', {'user': user, 'bookings': bookings})


@login_required
@user_passes_test(is_admin)
def admin_services(request):
    photography_packages = PhotographyPackage.objects.all()
    catering_packages = CateringPackage.objects.all()
    return render(request, 'events/admin/services.html', {
        'photography_packages': photography_packages,
        'catering_packages': catering_packages,
    })


@login_required
@user_passes_test(is_admin)
def admin_photography_create(request):
    if request.method == 'POST':
        form = PhotographyPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photography package created successfully!')
            return redirect('admin_services')
    else:
        form = PhotographyPackageForm()
    
    return render(request, 'events/admin/service_form.html', {
        'form': form,
        'title': 'Create Photography Package',
        'service_type': 'photography'
    })


@login_required
@user_passes_test(is_admin)
def admin_catering_create(request):
    if request.method == 'POST':
        form = CateringPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catering package created successfully!')
            return redirect('admin_services')
    else:
        form = CateringPackageForm()
    
    return render(request, 'events/admin/service_form.html', {
        'form': form,
        'title': 'Create Catering Package',
        'service_type': 'catering'
    })

