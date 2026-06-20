from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class BannedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            profile = getattr(request.user, 'profile', None)
            if profile and profile.is_banned:
                logout(request)
                messages.error(
                    request,
                    f'Ваш аккаунт заблокирован. {profile.ban_reason or "Обратитесь в поддержку."}',
                )
                return redirect(reverse('login'))
        return self.get_response(request)
