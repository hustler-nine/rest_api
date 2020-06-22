from django import template
from django.contrib.auth.models import User
from online_users.models import OnlineUserActivity
from datetime import timedelta

register = template.Library()


@register.filter(name='is_active')
def is_active(request):
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=60))
    active_users = (user for user in user_activity_objects)
    users = User.objects.exclude(username=request.user.username)
    for user in users:
        if user in active_users:
            return True
        else:
            return False


