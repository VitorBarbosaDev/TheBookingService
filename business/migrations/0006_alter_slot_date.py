# Generated by Django 4.2.8 on 2024-04-20 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_slot_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]