from .club_data import CLUB


def club_context(request):
    profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    is_site_admin = (
        request.user.is_authenticated
        and (request.user.is_superuser or (profile and profile.is_site_admin))
    )
    return {
        **CLUB,
        'is_site_admin': is_site_admin,
    }
