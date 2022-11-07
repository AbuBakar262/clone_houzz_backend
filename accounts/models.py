from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from accounts.usermanager import UserManager

ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Professional', 'Professional'),
        ('Client', 'Client')
    )
GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)


class User(AbstractBaseUser, PermissionsMixin):
    gender = models.CharField(_('gender choice'), max_length=25, choices=GENDER_CHOICES)
    role = models.CharField(_('select role'), max_length=15, choices=ROLE_CHOICES)
    username = models.CharField(_('username'), max_length=20, unique=True)
    email = models.EmailField(_("email address"), max_length=25, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active status"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    phone_number = models.CharField(_("phone number"), unique=True, max_length=15, null=True, blank=True)
    terms_conditions = models.BooleanField(_("terms & conditions"), default=False)
    profile_img = models.ImageField(_("profile pic"), upload_to=None, null=True, blank=True)
    is_blocked = models.BooleanField(_("blocked"), default=False)
    home_address = models.CharField(_("home address"), max_length=50, null=True, blank=True)
    approved = models.BooleanField(_("approved"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Company(models.Model):
    pro_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company', limit_choices_to={'role': 'Professional'})
    email = models.EmailField(_("email address"), max_length=25, unique=True, null=True, blank=True)
    name = models.CharField(_("company name"), max_length=50, null=True, blank=True)
    address = models.CharField(_("company address"), max_length=50, null=True, blank=True)
    license_number = models.CharField(_("license number"), max_length=50, null=True, blank=True)
    logo = models.ImageField(_("company logo"), upload_to=None, null=True, blank=True)
    about_us = models.TextField(_("about us"), null=True, blank=True)
    service_available_in = ArrayField(models.CharField(_("service available in"), max_length=50, null=True,
                                            blank=True), size=10, null=True, blank=True)
    worker_count = models.CharField(_("worker count"), max_length=50, null=True, blank=True)
    completed_projects = models.CharField(_("completed projects"), max_length=50, null=True,
                                            blank=True)
    experience = models.CharField(_("experience"), max_length=50, null=True, blank=True)
    approved = models.BooleanField(_("approved"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.name


class Projects(models.Model):
    pro_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pro_user', limit_choices_to={'role': 'Professional'})
    title = models.CharField(_("title"), max_length=50, null=True, blank=True)
    location = models.CharField(_("location"), max_length=50, null=True, blank=True)
    description = models.TextField(_("description"), max_length=50, null=True, blank=True)
    image = models.ImageField(_("images"), upload_to=None, null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.title
