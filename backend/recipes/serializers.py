from django.shortcuts import get_object_or_404
import webcolors

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.models import User

from .models import (
    Ingredient,
    AmountOfIngrediend,
    Recipe,
    Tag,
    Favourite,
    CartShopping
)
from users.serializers import CustomUserSerializer

class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    
    color = Hex2NameColor()
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    
    id = serializers.ReadOnlyField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
        read_only=True
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = AmountOfIngrediend
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit'
        )


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(
        many=False,
        read_only=True
    )
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    image = Base64ImageField()
    ingredients = IngredientForRecipeSerializer(
        source='amountofingrediend_set',
        many=True,
        read_only=True,
    )
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = (
            'is_favorited',
            'is_in_shopping_cart'
        )


    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favourite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return CartShopping.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['id']
            )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data
        )
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        for ingredient in ingredients_data:
            AmountOfIngrediend.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        recipe.save()
        return recipe