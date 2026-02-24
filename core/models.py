from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from uuid import uuid4


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        if not password:
            raise ValueError("Users must have a password")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False,verbose_name="user id:")
    email = models.EmailField(unique=True, max_length=255,null=False, blank=False,verbose_name="emial address:")
    name = models.CharField(max_length=255, verbose_name="full name:")
    is_active = models.BooleanField(default=True,verbose_name="is active:")
    is_staff = models.BooleanField(default=False,verbose_name="is_staff")
    date_joined = models.DateTimeField(default=timezone.now,verbose_name="created time:")
    # if you use deafult+timezone.now it can be override after create
    # else if you use auto_now_add=True it can't override after create
    updated_time = models.DateTimeField(auto_now=True,verbose_name="updated time:")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] # don't forget this field is require for superuser :)

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return f"{self.name} ({self.email})"
