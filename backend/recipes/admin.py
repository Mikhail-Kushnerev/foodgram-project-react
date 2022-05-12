from api.utils import IngredientFilter
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (AmountOfIngrediend, CartShopping, Favourite, Ingredient,
                     Recipe, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color'
    )
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = (IngredientFilter,)
    ordering = ('name',)
    list_per_page = 20


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'preview',
        'get_text',
        'favorites_count'
    )
    list_filter = (
        'author',
        'tags'
    )
    search_fields = (
        'name',
        'text'
    )
    ordering = ('author',)
    read_only_fields = ('preview',)
    list_per_page = 20

    def preview(self, obj):
        return mark_safe(
            f"<img src='{obj.image.url}' width='50' height='60'>"
        )

    def favorites_count(self, obj):
        return obj.favourites.count()


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    list_filter = (
        'user',
    )
    search_fields = ('recipe',)
    list_per_page = 20


@admin.register(AmountOfIngrediend)
class AmountOfIngrediendAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
    list_editable = ('amount',)
    list_filter = ('recipe__author',)
    ordering = ['-recipe']
    list_per_page = 20


@admin.register(CartShopping)
class CartShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
