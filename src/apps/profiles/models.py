from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as t
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from src.apps.common.models import BaseEntityModel

User = get_user_model()


class Profile(BaseEntityModel):
    class Gender(models.TextChoices):
        MALE = "M", t("Male")
        FEMALE = "F", t("Female")
        NON_BINARY = "NB", t("Non-binary")
        OTHER = "O", t("Other")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(verbose_name=t("Phone Number"), max_length=30, default="+11111111111")
    about_me = models.TextField(verbose_name=t("About Me"), default="Say something about yourself!")
    gender = models.CharField(
        verbose_name=t("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(verbose_name=t("Country"), blank=True)
    city = models.CharField(verbose_name=t("City"), max_length=255, blank=True)
    profile_photo = models.ImageField(
        verbose_name=t("Profile Photo"),
        default="default_photos/profile.png",
    )
    twitter_handle = models.CharField(verbose_name=t("Twitter Handle"), max_length=255, blank=True)
    followers = models.ManyToManyField("self", related_name="following", blank=True, symmetrical=False)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

    def follow(self, profile):
        self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)

    def is_following(self, profile) -> bool:
        return self.following.filter(_id=profile._id).exists()

    def is_follower(self, profile) -> bool:
        return profile.followers.filter(_id=self._id).exists()
