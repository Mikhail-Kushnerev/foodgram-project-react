import base64
from django.shortcuts import get_object_or_404
import webcolors

from PIL import Image
from io import BytesIO
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Ingredient,
    AmountOfIngrediend,
    Recipe,
    Tag
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

class Img2Base64(serializers.Field):
    def to_internal_value(self, data):
        with open(data, 'rb') as file:
            data = BytesIO(base64.b64decode(file.read()))
        # image = Image.open(BytesIO(base64.b64decode(data)))
        # image = image.save('image.jpeg', 'JPEG')
        image = Image.open(data)
        return image

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


class IngredientForRecipeCreate(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField(
    #     source='ingredient.id',
    #     read_only=True
    # )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    # amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = AmountOfIngrediend
        fields = ['id', 'amount']

    # def to_representation(self, instance):
    #     ingredient_in_recipe = [
    #         item for item in
    #         AmountOfIngrediend.objects.filter(
    #             ingredient=instance
    #         )
    #     ]
    #     return IngredientForRecipeSerializer(ingredient_in_recipe).data

class RecipeSerializer(serializers.ModelSerializer):
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


    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что значение количества '
                                    'ингредиента больше 0')
                })
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            AmountOfIngrediend.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe