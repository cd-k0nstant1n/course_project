from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Appointment, Code


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = "phones", "dates_of_birth", "specialties"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [CustomUserInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Appointment)
admin.site.register(CustomUser)
admin.site.register(Code)

