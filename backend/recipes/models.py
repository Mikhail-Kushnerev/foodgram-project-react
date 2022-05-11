from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False
    )
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='AmountOfIngrediend'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='Такой рецепт уже создавался Вами!'
            )
        ]
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_text(self):
        return self.text[:100]
    get_text.short_description = "Описание"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200
    )
    measurement_unit = models.CharField(
        max_length=200,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AmountOfIngrediend(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        default=1,
        validators=(MinValueValidator(1),),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='Использовать один ингредиент более 1-го раза нельзя!'
            )
        ]

    def __str__(self):
        return self.recipe.name


class Tag(models.Model):
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'

    COLOR_CHOICES = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Синий'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        choices=COLOR_CHOICES
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'slug'),
                name='Поле <slug> должно не повторять поле <name>!'
            )
        ]

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Рецепт уже находится в избранном!'
            )
        ]


class CartShopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_shoppings'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_shoppings'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='Рецепт уже находится в корзине!'
            )
        ]

    def __str__(self) -> str:
        return self.recipe.name
