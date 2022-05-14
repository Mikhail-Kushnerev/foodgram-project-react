from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (AmountOfIngrediend, CartShopping, Favourite,
                            Ingredient, Recipe, Tag)
from users.models import User
from .fields import Hex2NameColor


class RecipeUser(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


class SubscriptionsSerializer(RecipeUser):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = (
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "password",
            "groups",
            "user_permissions"
        )

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return RecipeUser(
            queryset,
            many=True
        ).data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.follower.filter(author=obj).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientForRecipeCreate(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    author = CustomUserSerializer(
        many=False,
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    ingredients = IngredientForRecipeCreate(
        source='amountofingrediend_set',
        many=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favourite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return CartShopping.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def validate(self, data):
        ingredients = data.pop('amountofingrediend_set')
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['ingredient']['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент уже добавлен'
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) <= 0:
                raise serializers.ValidationError(
                    'Убедитесь, что значение количества ингредиента больше 0'
                )
        data['ingredients'] = ingredients
        return data

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            AmountOfIngrediend.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'])

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.add_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('amountofingrediend_set')
        super().update(instance, validated_data)
        AmountOfIngrediend.objects.filter(
            recipe=instance
        ).all().delete()
        self.add_ingredients(ingredients_data, instance)
        instance.save()
        return instance


class RecipeSerializerGet(RecipeSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
