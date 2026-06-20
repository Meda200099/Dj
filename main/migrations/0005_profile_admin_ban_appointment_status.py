# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_delete_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ban_reason',
            field=models.TextField(blank=True, verbose_name='Причина блокировки'),
        ),
        migrations.AddField(
            model_name='profile',
            name='banned_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата блокировки'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_banned',
            field=models.BooleanField(default=False, verbose_name='Заблокирован'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_site_admin',
            field=models.BooleanField(default=False, verbose_name='Администратор сайта'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Ожидает'),
                    ('confirmed', 'Подтверждена'),
                    ('cancelled', 'Отменена'),
                ],
                default='pending',
                max_length=20,
                verbose_name='Статус',
            ),
        ),
    ]
