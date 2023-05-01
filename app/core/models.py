"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from phonenumber_field.modelfields import PhoneNumberField


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
    identification = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    working_status = models.CharField(max_length=20)
    home_address = models.CharField(max_length=255)
    work_address = models.CharField(max_length=255)
    mob_phone = PhoneNumberField(region='EG')
    home_phone = PhoneNumberField(null=True, blank=True, region='EG')
    marital_status = models.CharField(max_length=25)
    family_count = models.PositiveIntegerField()
    kids_count = models.PositiveIntegerField()
    avg_income = models.DecimalField(max_digits=10, decimal_places=2)
    gallery = models.ManyToManyField('core.Image', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.name


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

    def __str__(self):
        return f'{self.inv_type} investigation ({self.inv_status})'


class Region(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.region}, {self.city}, {self.province}"
