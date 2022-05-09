from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'last_name',
        'first_name'
    )
    search_fields = ('username',)
    list_filter = ('email',)
    list_per_page = 20


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
    list_per_page = 20
