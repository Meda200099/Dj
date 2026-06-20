from django.contrib import admin
from django.contrib.auth.decorators import login_required
from .models import Profile, Appointment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_site_admin', 'is_banned', 'banned_at')
    list_filter = ('is_site_admin', 'is_banned')
    search_fields = ('user__username', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'tariff', 'seat', 'appointment_date',
        'appointment_time', 'status', 'created_at',
    )
    list_filter = ('tariff', 'appointment_date', 'status')
    search_fields = ('user__username', 'seat', 'tariff')

@login_required  
def dashboard_view(request):
    
    profile = request.user.profile 
    
 
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date')
