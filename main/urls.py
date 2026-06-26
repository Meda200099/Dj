from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('katalog/', views.catalog_view, name='catalog'),
    path('tarify/<slug:slug>/', views.tariff_detail, name='tariff_detail'),
    path('register/', views.register_view, name='register'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('profile/', views.profile_view, name='profile'),
    path('panel/', views.admin_panel_view, name='admin_panel'),
    path('analytics/catalog-ping/', views.catalog_session_ping, name='catalog_session_ping'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
