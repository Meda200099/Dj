from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from django.db.models import Count, Q

from .models import Profile, Appointment
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


def catalog_view(request):
    zone = request.GET.get("zone", "all")
    computers = get_computers_by_zone(zone)
    data = {
        **_club_context(),
        "computers": computers,
        "zones": ZONES,
        "zone_filters": ZONE_FILTERS,
        "active_zone": zone,
        "total_seats": len(SEATS),
    }
    return render(request, "main/catalog.html", data)


def tariff_detail(request, slug):
    tariff = get_tariff(slug)
    if tariff is None:
        raise Http404("Тариф не найден")
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
        elif len(password or "") < 8:
            error = "Пароль должен быть не короче 8 символов"
        elif password != password2:
            error = "Пароли не совпадают"
        elif User.objects.filter(username=username).exists():
            error = "Такой логин уже занят"
        else:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = full_name
            user.save()
            Profile.objects.create(user=user, phone=phone)
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
                    conflict = Appointment.objects.filter(
                        seat=selected_seat,
                        appointment_date=selected_date,
                        appointment_time=selected_time,
                        status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
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

    users_qs = User.objects.select_related("profile").order_by("-date_joined")
    if search:
        users_qs = users_qs.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(profile__phone__icontains=search)
        )

    appointments_qs = Appointment.objects.select_related("user").order_by("-created_at")
    if tab == "appointments":
        status_filter = request.GET.get("status", "")
        if status_filter:
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

        return redirect(f"{request.path}?tab={tab}" + (f"&q={search}" if search else ""))

    stats = {
        "users_total": User.objects.count(),
        "users_banned": Profile.objects.filter(is_banned=True).count(),
        "admins_total": Profile.objects.filter(is_site_admin=True).count(),
        "appointments_total": Appointment.objects.count(),
        "appointments_pending": Appointment.objects.filter(status=Appointment.STATUS_PENDING).count(),
        "appointments_today": Appointment.objects.filter(appointment_date=date.today()).count(),
    }

    return render(request, "main/admin_panel.html", {
        **_club_context(),
        "tab": tab,
        "search": search,
        "users": users_qs[:50],
        "appointments": appointments_qs[:50],
        "stats": stats,
        "status_choices": Appointment.STATUS_CHOICES,
    })


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
                next_url = request.GET.get("next") or "appointment"
                return redirect(next_url)
        else:
            error = "Неверный логин или пароль"

    return render(request, "main/login.html", {**_club_context(), "error": error})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("index")


def page_not_found_view(request, exception):
    return render(request, "main/404.html", _club_context(), status=404)
