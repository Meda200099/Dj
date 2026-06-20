from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def site_admin_required(view_func):
    @login_required(login_url='login')
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if request.user.is_superuser or (profile and profile.is_site_admin):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Доступ только для администраторов.')
        return redirect('index')
    return wrapper
