from django.contrib import admin
from .models import Profile


class ProfileAdminConf(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(Profile, ProfileAdminConf)
