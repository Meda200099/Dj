from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Телефон', max_length=20)

    def __str__(self):
        
        return f'{self.user.get_full_name() or self.user.username} — {self.phone}'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.CharField('Услуга', max_length=120)
    appointment_date = models.DateField('Дата приёма')
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.service} ({self.appointment_date})'
