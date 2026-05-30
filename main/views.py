from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import Http404

from .models import Profile, Appointment

from .clinic_data import (

    CLINIC,

    BOOKING_BUTTONS,

    SERVICES,

    PRICES,

    SPECIALISTS,

    EQUIPMENT,

    get_service,

)





def _clinic_context():

    return {**CLINIC}





def index(request):

    data = {

        **_clinic_context(),

        "booking_buttons": BOOKING_BUTTONS,

        "services": SERVICES,

        "prices": PRICES,

        "specialists": SPECIALISTS,

        "equipment": EQUIPMENT,

    }

    return render(request, "main/index.html", data)





def service_detail(request, slug):

    service = get_service(slug)

    if service is None:

        raise Http404("Услуга не найдена")

    data = {

        **_clinic_context(),

        "service": service,

    }

    return render(request, "main/service.html", data)





def menu(request):

    data = {

        "title": "Главная страница",

        "values": ["Python", "Django", "PostgreSQL"],

    }

    return render(request, "main/gs.html", data)





def register_view(request):

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
            return redirect("appointment")

    return render(request, "main/register.html", {
        **_clinic_context(),
        "error": error,
        "full_name": full_name,
        "phone": phone,
        "username": username,
    })


@login_required(login_url="login")
def appointment_view(request):

    error = None
    success = None
    selected_service = request.GET.get("service", "")
    selected_date = ""
    selected_comment = ""

    profile = getattr(request.user, "profile", None)
    patient_name = request.user.first_name or request.user.username
    patient_phone = profile.phone if profile else "—"

    if request.method == "POST":
        selected_service = request.POST.get("service", "").strip()
        selected_date = request.POST.get("date", "").strip()
        selected_comment = request.POST.get("comment", "").strip()

        if not selected_service:
            error = "Выберите вид услуги"
        elif not selected_date:
            error = "Укажите дату назначения"
        else:
            Appointment.objects.create(
                user=request.user,
                service=selected_service,
                appointment_date=selected_date,
                comment=selected_comment,
            )
            success = "Спасибо! Мы свяжемся с вами для подтверждения записи."
            selected_service = ""
            selected_date = ""
            selected_comment = ""

    return render(request, "main/appointment.html", {
        **_clinic_context(),
        "services": SERVICES,
        "error": error,
        "success": success,
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "selected_service": selected_service,
        "selected_date": selected_date,
        "selected_comment": selected_comment,
    })





def login_view(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("appointment")

        else:

            error = "Неверный логин или пароль"

    return render(request, "main/login.html", {**_clinic_context(), "error": error})





def logout_view(request):

    logout(request)

    return redirect("index")

