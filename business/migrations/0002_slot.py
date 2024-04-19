# Generated by Django 4.2.8 on 2024-04-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_booked', models.BooleanField(default=False)),
                ('business_hours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='business.businesshours')),
            ],
        ),
    ]
