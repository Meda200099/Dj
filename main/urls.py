from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uslugi/<slug:slug>/', views.service_detail, name='service_detail'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register_view, name='register'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]