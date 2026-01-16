from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Event, Booking, BookingService, PhotographyPackage, CateringPackage, UserProfile, EventCategory


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                role='user'
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()


class EventSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search events...'}))
    category = forms.ModelChoiceField(queryset=None, required=False, empty_label='All Categories')
    event_type = forms.ChoiceField(choices=[('', 'All Types')] + Event.EVENT_TYPES, required=False)
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Location...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = EventCategory.objects.all()


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['notes']


class PhotographyServiceForm(forms.Form):
    package = forms.ModelChoiceField(queryset=PhotographyPackage.objects.filter(is_active=True), required=False)
    photo_type = forms.ChoiceField(choices=PhotographyPackage.PHOTO_TYPES, required=False)
    duration = forms.ChoiceField(choices=PhotographyPackage.DURATION_CHOICES, required=False)
    delivery_method = forms.ChoiceField(choices=PhotographyPackage.DELIVERY_CHOICES, required=False)


class CateringServiceForm(forms.Form):
    package = forms.ModelChoiceField(queryset=CateringPackage.objects.filter(is_active=True), required=False)
    food_type = forms.ChoiceField(choices=[
        ('', 'Select Food Type'),
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
        ('both', 'Both'),
    ], required=False)
    plate_count = forms.IntegerField(required=False, min_value=1)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'event_type', 'date', 'time',
                  'location', 'organizer', 'price', 'capacity', 'image', 'video', 'registration_enabled']


class PhotographyPackageForm(forms.ModelForm):
    class Meta:
        model = PhotographyPackage
        fields = ['name', 'description', 'photo_count', 'price', 'photographers_count',
                  'includes_editing', 'includes_album', 'is_active']


class CateringPackageForm(forms.ModelForm):
    class Meta:
        model = CateringPackage
        fields = ['name', 'description', 'meal_type', 'price_per_plate', 'supports_veg',
                  'supports_nonveg', 'menu_type', 'is_active']

