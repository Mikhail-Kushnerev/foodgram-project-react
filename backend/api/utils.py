import webcolors

from rest_framework import serializers

from recipes.models import Recipe

class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class RecipeUser(serializers.ModelSerializer):
    class Meta:
        model  = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
