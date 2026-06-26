from datetime import date, timedelta
from urllib.parse import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Profile, Appointment, CatalogSession, TariffPageView
from .analytics import get_analytics_context
from .decorators import site_admin_required
from .club_data import (
    CLUB,
    BOOKING_BUTTONS,
    TARIFFS,
    PRICES,
    SEATS,
    ZONES,
    PERIPHERALS,
    FAQ,
    ZONE_FILTERS,
    get_tariff,
    get_computers_by_zone,
    get_seats_for_tariff,
)

VALID_TARIFFS = {t["title"] for t in TARIFFS}


def _club_context():
    return {**CLUB}


def _get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"phone": "—"},
    )
    return profile


def _is_banned(user):
    if user.is_superuser:
        return False
    profile = getattr(user, "profile", None)
    return profile is not None and profile.is_banned


def index(request):
    data = {
        **_club_context(),
        "booking_buttons": BOOKING_BUTTONS,
        "tariffs": TARIFFS,
        "prices": PRICES,
        "zones": ZONES,
        "peripherals": PERIPHERALS,
        "faq": FAQ,
    }
    return render(request, "main/index.html", data)


def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _admin_panel_redirect_url(tab, search="", status_filter=""):
    params = {"tab": tab}
    if search:
        params["q"] = search
    if tab == "appointments" and status_filter:
        params["status"] = status_filter
    return f"?{urlencode(params)}"


def _safe_next_redirect(request, fallback="appointment"):
    next_url = request.GET.get("next") or request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect(fallback)


def catalog_view(request):
    zone = request.GET.get("zone", "all")
    computers = get_computers_by_zone(zone)
    session_key = _ensure_session_key(request)
    zone_key = zone or "all"
    cutoff = timezone.now() - timedelta(minutes=30)
    catalog_session = CatalogSession.objects.filter(
        session_key=session_key,
        zone=zone_key,
        started_at__gte=cutoff,
    ).order_by("-started_at").first()
    if catalog_session is None:
        catalog_session = CatalogSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key,
            zone=zone_key,
        )
    data = {
        **_club_context(),
        "computers": computers,
        "zones": ZONES,
        "zone_filters": ZONE_FILTERS,
        "active_zone": zone,
        "total_seats": len(SEATS),
        "catalog_session_id": catalog_session.pk,
    }
    return render(request, "main/catalog.html", data)


def tariff_detail(request, slug):
    tariff = get_tariff(slug)
    if tariff is None:
        raise Http404("Тариф не найден")
    TariffPageView.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=_ensure_session_key(request),
        tariff=tariff["title"],
    )
    data = {
        **_club_context(),
        "tariff": tariff,
    }
    return render(request, "main/tariff.html", data)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("appointment")

    error = None
    full_name = ""
    phone = ""
    username = ""

    if request.method == "POST":
        full_name = (request.POST.get("full_name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not full_name:
            error = "Укажите ваше имя"
        elif not phone:
            error = "Укажите телефон"
        elif not username:
            error = "Укажите логин"
        elif len(username) < 3:
            error = "Логин должен быть не короче 3 символов"
        elif len(password or "") < 8:
            error = "Пароль должен быть не короче 8 символов"
        elif password != password2:
            error = "Пароли не совпадают"
        elif User.objects.filter(username=username).exists():
            error = "Такой логин уже занят"
        else:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = full_name
                    user.save()
                    Profile.objects.create(user=user, phone=phone)
            except ValidationError:
                error = "Некорректный логин"
            else:
                login(request, user)
                messages.success(request, "Добро пожаловать! Теперь можно забронировать место.")
                return redirect("appointment")

    return render(request, "main/register.html", {
        **_club_context(),
        "error": error,
        "full_name": full_name,
        "phone": phone,
        "username": username,
    })


@login_required(login_url="login")
def appointment_view(request):
    if _is_banned(request.user):
        logout(request)
        messages.error(request, "Ваш аккаунт заблокирован.")
        return redirect("login")

    error = None
    selected_tariff = request.GET.get("tariff", "")
    selected_seat = request.GET.get("seat", "")
    if selected_tariff and selected_tariff not in VALID_TARIFFS:
        selected_tariff = ""
    selected_date = ""
    selected_time = ""
    selected_comment = ""

    profile = _get_or_create_profile(request.user)
    player_name = request.user.first_name or request.user.username
    player_phone = profile.phone

    available_seats = get_seats_for_tariff(selected_tariff) if selected_tariff else SEATS

    if request.method == "POST":
        selected_tariff = request.POST.get("tariff", "").strip()
        selected_seat = request.POST.get("seat", "").strip()
        selected_date = request.POST.get("date", "").strip()
        selected_time = request.POST.get("time", "").strip()
        selected_comment = request.POST.get("comment", "").strip()
        available_seats = get_seats_for_tariff(selected_tariff) if selected_tariff else SEATS

        valid_seat_values = {s["value"] for s in available_seats}

        if not selected_tariff:
            error = "Выберите тариф"
        elif selected_tariff not in VALID_TARIFFS:
            error = "Выберите корректный тариф"
        elif not selected_seat or selected_seat not in valid_seat_values:
            error = "Выберите корректное место для выбранного тарифа"
        elif not selected_date:
            error = "Укажите дату"
        elif not selected_time:
            error = "Укажите время"
        else:
            try:
                booking_date = date.fromisoformat(selected_date)
            except ValueError:
                error = "Некорректная дата"
            else:
                if booking_date < date.today():
                    error = "Нельзя бронировать на прошедшую дату"
                else:
                    with transaction.atomic():
                        conflict = Appointment.objects.select_for_update().filter(
                            seat=selected_seat,
                            appointment_date=selected_date,
                            appointment_time=selected_time,
                            status__in=[
                                Appointment.STATUS_PENDING,
                                Appointment.STATUS_CONFIRMED,
                            ],
                        ).exists()
                        if conflict:
                            error = "Это место уже занято на выбранное время"
                        else:
                            Appointment.objects.create(
                                user=request.user,
                                tariff=selected_tariff,
                                seat=selected_seat,
                                appointment_date=selected_date,
                                appointment_time=selected_time,
                                comment=selected_comment,
                            )
                    if not error:
                        messages.success(
                            request,
                            "Заявка принята! Мы подтвердим бронь в ближайшее время.",
                        )
                        return redirect("profile")

    return render(request, "main/appointment.html", {
        **_club_context(),
        "tariffs": TARIFFS,
        "seats": available_seats,
        "all_seats_count": len(SEATS),
        "error": error,
        "player_name": player_name,
        "player_phone": player_phone,
        "selected_tariff": selected_tariff,
        "selected_seat": selected_seat,
        "selected_date": selected_date,
        "selected_time": selected_time,
        "selected_comment": selected_comment,
    })


@login_required(login_url="login")
def profile_view(request):
    if _is_banned(request.user):
        logout(request)
        messages.error(request, "Ваш аккаунт заблокирован.")
        return redirect("login")

    profile = _get_or_create_profile(request.user)
    appointments = request.user.appointments.all()

    if request.method == "POST" and request.POST.get("action") == "cancel":
        appt_id = request.POST.get("appointment_id")
        appointment = get_object_or_404(Appointment, pk=appt_id, user=request.user)
        if appointment.status != Appointment.STATUS_CANCELLED:
            appointment.status = Appointment.STATUS_CANCELLED
            appointment.save(update_fields=["status"])
            messages.success(request, f"Бронь {appointment.seat} отменена.")

    return render(request, "main/profile.html", {
        **_club_context(),
        "profile": profile,
        "appointments": appointments,
    })


@site_admin_required
def admin_panel_view(request):
    tab = request.GET.get("tab", "overview")
    search = (request.GET.get("q") or "").strip()
    status_filter = request.GET.get("status", "")

    users_qs = User.objects.select_related("profile").order_by("-date_joined")
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(profile__phone__icontains=search)
        )

    appointments_qs = Appointment.objects.select_related("user").order_by("-created_at")
    if tab == "appointments" and status_filter:
        appointments_qs = appointments_qs.filter(status=status_filter)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "toggle_admin":
            user_id = request.POST.get("user_id")
            target = get_object_or_404(User, pk=user_id)
            if target == request.user:
                messages.error(request, "Нельзя изменить свои права.")
            elif target.is_superuser:
                messages.error(request, "Нельзя изменять права суперпользователя Django.")
            else:
                profile = _get_or_create_profile(target)
                profile.is_site_admin = not profile.is_site_admin
                profile.save(update_fields=["is_site_admin"])
                state = "назначен" if profile.is_site_admin else "снят"
                messages.success(request, f"Пользователь {target.username}: админ {state}.")

        elif action == "toggle_ban":
            user_id = request.POST.get("user_id")
            target = get_object_or_404(User, pk=user_id)
            if target == request.user:
                messages.error(request, "Нельзя заблокировать себя.")
            elif target.is_superuser:
                messages.error(request, "Нельзя заблокировать суперпользователя.")
            else:
                profile = _get_or_create_profile(target)
                profile.is_banned = not profile.is_banned
                if profile.is_banned:
                    profile.banned_at = timezone.now()
                    profile.ban_reason = (request.POST.get("ban_reason") or "").strip()
                else:
                    profile.banned_at = None
                    profile.ban_reason = ""
                profile.save()
                state = "заблокирован" if profile.is_banned else "разблокирован"
                messages.success(request, f"Пользователь {target.username} {state}.")

        elif action == "set_appointment_status":
            appt_id = request.POST.get("appointment_id")
            new_status = request.POST.get("status")
            appointment = get_object_or_404(Appointment, pk=appt_id)
            if new_status in dict(Appointment.STATUS_CHOICES):
                appointment.status = new_status
                appointment.save(update_fields=["status"])
                messages.success(request, f"Статус брони #{appointment.pk} обновлён.")

        return redirect(request.path + _admin_panel_redirect_url(tab, search, status_filter))

    stats = {
        "users_total": User.objects.count(),
        "users_banned": Profile.objects.filter(is_banned=True).count(),
        "admins_total": User.objects.filter(
            Q(is_superuser=True) | Q(profile__is_site_admin=True)
        ).distinct().count(),
        "appointments_total": Appointment.objects.count(),
        "appointments_pending": Appointment.objects.filter(status=Appointment.STATUS_PENDING).count(),
        "appointments_today": Appointment.objects.filter(
            appointment_date=date.today(),
        ).exclude(status=Appointment.STATUS_CANCELLED).count(),
    }

    analytics = get_analytics_context() if tab == "analytics" else None

    return render(request, "main/admin_panel.html", {
        **_club_context(),
        "tab": tab,
        "search": search,
        "status_filter": status_filter,
        "users": users_qs[:50],
        "appointments": appointments_qs[:50],
        "stats": stats,
        "analytics": analytics,
        "status_choices": Appointment.STATUS_CHOICES,
    })


@require_POST
def catalog_session_ping(request):
    session_id = request.POST.get("session_id")
    try:
        duration = int(request.POST.get("duration", 0))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid_duration"}, status=400)

    if duration < 0 or duration > 86400:
        return JsonResponse({"ok": False, "error": "invalid_duration"}, status=400)

    session_key = _ensure_session_key(request)
    try:
        catalog_session = CatalogSession.objects.get(pk=session_id, session_key=session_key)
    except (CatalogSession.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"ok": False, "error": "not_found"}, status=404)

    if duration > catalog_session.duration_seconds:
        catalog_session.duration_seconds = duration
        catalog_session.save(update_fields=["duration_seconds"])

    return JsonResponse({"ok": True})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("appointment")

    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile = getattr(user, "profile", None)
            if profile and profile.is_banned and not user.is_superuser:
                reason = profile.ban_reason or "Обратитесь в поддержку."
                error = f"Аккаунт заблокирован. {reason}"
            else:
                login(request, user)
                messages.success(request, f"С возвращением, {user.first_name or user.username}!")
                return _safe_next_redirect(request)
        else:
            error = "Неверный логин или пароль"

    return render(request, "main/login.html", {**_club_context(), "error": error})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("index")


def page_not_found_view(request, exception):
    return render(request, "main/404.html", _club_context(), status=404)
