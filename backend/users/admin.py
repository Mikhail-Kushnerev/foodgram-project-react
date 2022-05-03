from django.contrib import admin

from .models import User, Subscription

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'last_name',
        'first_name'
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
