from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Телефон', max_length=20)
    is_site_admin = models.BooleanField('Администратор сайта', default=False)
    is_banned = models.BooleanField('Заблокирован', default=False)
    ban_reason = models.TextField('Причина блокировки', blank=True)
    banned_at = models.DateTimeField('Дата блокировки', null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.phone}'

    @property
    def can_access_admin(self):
        return self.user.is_superuser or self.is_site_admin


class Appointment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_CONFIRMED, 'Подтверждена'),
        (STATUS_CANCELLED, 'Отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    tariff = models.CharField('Тариф', max_length=120)
    seat = models.CharField('Место', max_length=20)
    appointment_date = models.DateField('Дата')
    appointment_time = models.TimeField('Время')
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time', '-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.tariff}, {self.seat} ({self.appointment_date} {self.appointment_time})'

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
