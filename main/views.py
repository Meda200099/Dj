from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.models import User

from django.http import Http404



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

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        password2 = request.POST.get("password2")

        if password != password2:

            error = "Пароли не совпадают"

        elif User.objects.filter(username=username).exists():

            error = "Такой логин уже занят"

        else:

            user = User.objects.create_user(username=username, password=password)

            login(request, user)

            return redirect("index")

    return render(request, "main/register.html", {**_clinic_context(), "error": error})





def login_view(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("index")

        else:

            error = "Неверный логин или пароль"

    return render(request, "main/login.html", {**_clinic_context(), "error": error})





def logout_view(request):

    logout(request)

    return redirect("index")

