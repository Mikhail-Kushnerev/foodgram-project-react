# Generated by Django 4.0.4 on 2022-05-14 16:51

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amountofingrediend',
            options={'verbose_name': 'Ингридиент рецепта', 'verbose_name_plural': 'Ингридиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='cartshopping',
            options={'verbose_name': 'Ингридиент в корзине', 'verbose_name_plural': 'Ингридиенты в корзине'},
        ),
        migrations.AlterModelOptions(
            name='favourite',
            options={'verbose_name': 'Категория "Избранное"', 'verbose_name_plural': 'Категория "Избранные"'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиент'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tэг', 'verbose_name_plural': 'Tэги'},
        ),
        migrations.AlterField(
            model_name='amountofingrediend',
            name='amount',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='кол-во ингридиента для рецепта'),
        ),
        migrations.AlterField(
            model_name='amountofingrediend',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='ингридиент рецепта'),
        ),
        migrations.AlterField(
            model_name='amountofingrediend',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепта'),
        ),
        migrations.AlterField(
            model_name='cartshopping',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_shoppings', to='recipes.recipe', verbose_name='Рецепт в корзине пользователя'),
        ),
        migrations.AlterField(
            model_name='cartshopping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_shoppings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавивший товар в корзину'),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipes.recipe', verbose_name='Избранный товар'),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Оценивший пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='Ед. изм.'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Наименование рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/', verbose_name='Изображение рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.AmountOfIngrediend', to='recipes.ingredient', verbose_name='Ингридиенты(и) рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.tag', verbose_name='Тэг(и) рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('#E26C2D', 'Оранжевый'), ('#49B64E', 'Зеленый'), ('#8775D2', 'Фиолетовый')], max_length=16, unique=True, verbose_name='Цвет тэга'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование тэга'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='SLUG тэга'),
        ),
    ]
