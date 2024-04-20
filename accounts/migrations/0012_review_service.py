# Generated by Django 4.2.8 on 2024-04-20 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_service_rating'),
        ('accounts', '0011_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='services.service'),
        ),
    ]
