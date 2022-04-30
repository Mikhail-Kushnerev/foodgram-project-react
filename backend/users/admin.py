from django.contrib import admin

from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'last_name',
        'first_name'
    )
# Register your models here.
