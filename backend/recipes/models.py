from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
    )
    text = models.TextField(verbose_name='Описание рецепта')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Изображение рецепта'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=False,
        verbose_name='Тэг(и) рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='AmountOfIngrediend',
        verbose_name='Ингридиенты(и) рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='Такой рецепт уже создавался Вами!'
            )
        ]
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name

    def get_text(self):
        return self.text[:100]
    get_text.short_description = "Описание"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование рецепта'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Ед. изм.'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиент'

    def __str__(self):
        return self.name


class AmountOfIngrediend(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингридиент рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепта'
    )
    amount = models.IntegerField(
        default=1,
        validators=(MinValueValidator(1),),
        verbose_name='кол-во ингридиента для рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='Использовать один ингредиент более 1-го раза нельзя!'
            )
        ]
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return self.recipe.name


class Tag(models.Model):
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'

    COLOR_CHOICES = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Наименование тэга'
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        choices=COLOR_CHOICES,
        verbose_name='Цвет тэга'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='SLUG тэга'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='Поле <slug> должно не повторять поле <name>!'
            )
        ]
        verbose_name = 'Tэг'
        verbose_name_plural = 'Tэги'

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Оценивший пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='Избранный товар'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Рецепт уже находится в избранном!'
            )
        ]
        verbose_name = 'Категория "Избранное"'
        verbose_name_plural = 'Категория "Избранные"'


class CartShopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_shoppings',
        verbose_name='Пользователь, добавивший товар в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_shoppings',
        verbose_name='Рецепт в корзине пользователя'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Рецепт уже находится в корзине!'
            )
        ]
        verbose_name = 'Ингридиент в корзине'
        verbose_name_plural = 'Ингридиенты в корзине'

    def __str__(self) -> str:
        return self.recipe.name
