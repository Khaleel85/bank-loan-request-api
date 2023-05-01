# Generated by Django 4.2 on 2023-04-30 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_image_alter_user_phone_requester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requester',
            name='age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='requester',
            name='identification',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='EG'),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv_status', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', max_length=10)),
                ('inv_type', models.CharField(choices=[('home', 'Home'), ('work', 'Work')], max_length=10)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('requester', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.requester')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]