from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed = (timezone.now().timestamp() - last_activity)
                if elapsed > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('login')
            request.session['last_activity'] = timezone.now().timestamp()
        
        response = self.get_response(request)
        return response

