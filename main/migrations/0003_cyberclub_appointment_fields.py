# Generated manually for cyber club redesign

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_appointment_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='service',
            new_name='tariff',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='tariff',
            field=models.CharField(max_length=120, verbose_name='Тариф'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='seat',
            field=models.CharField(default='S-01', max_length=20, verbose_name='Место'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.TimeField(default='12:00', verbose_name='Время'),
            preserve_default=False,
        ),
    ]
