"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator

from phonenumber_field.modelfields import PhoneNumberField

import phonenumbers

def investigation_image_file_path(instance, filename):
    ext = os.path.splittext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'investigation', filename)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    phone = PhoneNumberField(region='EG')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Requester(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    identification = models.PositiveIntegerField(unique=True)
    age = models.PositiveIntegerField()
    working_status = models.CharField(max_length=20)
    home_address = models.TextField(max_length=255)
    work_address = models.TextField(max_length=255)
    mob_phone = PhoneNumberField(region='EG', max_length=13, unique=True)

    # home_phone_regex = '^\+20[0-9]{8}$'
    # home_phone_validator = RegexValidator(
    #     regex=home_phone_regex,
    #     message='Home phone number must be in the format +20xxxxxxxx'

    # )
    home_phone = models.PositiveIntegerField(null=True)
    marital_status = models.CharField(max_length=25)
    family_count = models.PositiveIntegerField()
    kids_count = models.PositiveIntegerField()
    avg_income = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    # def clean(self):
    #     super().clean()
    #     try:
    #         parsed_phone = phonenumbers.parse(self.home_phone, 'EG')
    #         if not phonenumbers.is_valid_number(parsed_phone):
    #             raise ValidationError('Invalid phone number')
    #         formatted_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
    #         self.home_phone = formatted_phone
    #     except phonenumbers.phonenumberutil.NumberParseException:
    #         raise ValidationError('Invalid phone number')

class Investigation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    INV_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    INV_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
    ]
    inv_status = models.CharField(max_length=10, choices=INV_STATUS_CHOICES, default='pending')
    inv_type = models.CharField(max_length=10, choices=INV_TYPE_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.OneToOneField('Requester', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to=investigation_image_file_path)

    def __str__(self):
        return f'{self.inv_type} investigation ({self.inv_status})'


class Images(models.Model):
    investigation = models.ForeignKey(Investigation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=investigation_image_file_path,
    )

    def __str__(self):
        return self.image.name


class Region(models.Model):
    PROVINCE_CHOICES = [
        ('Alexandria', 'Alexandria'),
        ('Aswan', 'Aswan'),
        ('Asyut', 'Asyut'),
        ('Beheira', 'Beheira'),
        ('Beni Suef', 'Beni Suef'),
        ('Cairo', 'Cairo'),
        ('Dakahlia', 'Dakahlia'),
        ('Damietta', 'Damietta'),
        ('Faiyum', 'Faiyum'),
        ('Gharbia', 'Gharbia'),
        ('Giza', 'Giza'),
        ('Ismailia', 'Ismailia'),
        ('Kafr El Sheikh', 'Kafr El Sheikh'),
        ('Luxor', 'Luxor'),
        ('Matrouh', 'Matrouh'),
        ('Minya', 'Minya'),
        ('Monufia', 'Monufia'),
        ('New Valley', 'New Valley'),
        ('North Sinai', 'North Sinai'),
        ('Port Said', 'Port Said'),
        ('Qalyubia', 'Qalyubia'),
        ('Qena', 'Qena'),
        ('Red Sea', 'Red Sea'),
        ('Sharqia', 'Sharqia'),
        ('Sohag', 'Sohag'),
        ('South Sinai', 'South Sinai'),
        ('Suez', 'Suez'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    province = models.CharField(max_length=100, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.region}, {self.city}, {self.province}"
