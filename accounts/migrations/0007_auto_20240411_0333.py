# Generated by Django 3.2.25 on 2024-04-11 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_service_business'),
        ('accounts', '0006_auto_20240411_0333'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Business',
        ),
        migrations.DeleteModel(
            name='BusinessHours',
        ),
    ]
