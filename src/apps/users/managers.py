from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as t


# Managers are basically repositories for the models they are associated with.
class CustomUserManager(BaseUserManager):
    def validate_email(self, email) -> None:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(t("Invalid email address."))

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not first_name:
            raise ValueError(t("First name is required."))
        elif not last_name:
            raise ValueError(t("Last name is required."))
        elif not email:
            raise ValueError(t("Email is required."))
        elif not password:
            raise ValueError(t("Password is required."))

        email = self.normalize_email(email)
        self.validate_email(email)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(t("Superuser must have is_staff=True."))
        elif extra_fields.get("is_superuser") is not True:
            raise ValueError(t("Superuser must have is_superuser=True."))
        elif extra_fields.get("is_active") is not True:
            raise ValueError(t("Superuser must have is_active=True."))

        return self.create_user(first_name, last_name, email, password, **extra_fields)
