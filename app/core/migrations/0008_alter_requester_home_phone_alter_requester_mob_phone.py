# Generated by Django 4.2 on 2023-05-03 01:34

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_requester_home_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requester',
            name='home_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=11, region='EG', unique=True),
        ),
        migrations.AlterField(
            model_name='requester',
            name='mob_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=13, region='EG', unique=True),
        ),
    ]
