from django.db import models
from django.core.validators import MinValueValidator

from users.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.TimeField()
    is_in_shopping_cart = models.BooleanField()
    is_favorited = models.BooleanField()
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField()
    tag = models.ForeignKey(
        'Tag',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        # on_delete=models.CASCADE
    )


class Ingredient(models.Model):
    text = models.CharField(max_length=200)


class Amount_of_Ingrediend(models.Model):
    measurement_unit = models.CharField(max_length=200)
    amount = models.IntegerField(
        default=1,
        validators=(MinValueValidator(1),),
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )
    color = models.CharField(max_length=16)
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
