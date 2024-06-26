# Generated by Django 3.2.25 on 2024-04-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('confirmed', 'Confirmed'), ('completed', 'Completed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', max_length=50),
        ),
    ]
