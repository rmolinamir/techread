from django.contrib import admin
from .models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "_id",
        "id",
        "user",
        "gender",
        "phone_number",
        "country",
        "city",
    ]
    list_display_links = ["_id", "id", "user"]
    list_filter = ["_id", "id"]


admin.site.register(Profile, ProfileAdmin)
