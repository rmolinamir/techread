import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as t
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = t("User")
        verbose_name_plural = t("Users")

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def short_name(self):
        return self.first_name

    _id = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    first_name = models.CharField(verbose_name=t("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=t("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=t("Email"), unique=True, db_index=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()
