import datetime
from django.core.cache import cache
from django.conf import settings

from .models import Profile


class ActiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            current_user = request.user
            try:
                Profile.objects.get(user=current_user)
            except Profile.DoesNotExist:
                Profile.objects.create(user=current_user)
            finally:
                cache.set('last_seen_%s' % current_user.username, now,
                          settings.USER_LASTSEEN_TIMEOUT)
        response = self.get_response(request)
        return response

