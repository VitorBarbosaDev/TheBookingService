# Generated by Django 4.2.8 on 2024-04-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_business_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
