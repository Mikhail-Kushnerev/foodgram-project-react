from django_filters.rest_framework import FilterSet

from recipes.models import Recipe

class UserRecipeFilter(FilterSet):
    class Meta:
        model = Recipe
        fields = ('author',)