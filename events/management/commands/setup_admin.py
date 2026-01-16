from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import UserProfile


class Command(BaseCommand):
    help = 'Set up admin user profile'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the admin user')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = 'admin'
            profile.phone = '0000000000'
            profile.address = 'Admin Address'
            profile.is_active = True
            profile.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Admin profile created for {username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Admin profile updated for {username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist. Please create the user first.'))

