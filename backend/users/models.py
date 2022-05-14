from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта пользователя'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Никнейм пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering=['-id']
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='Вы уже подписывались на данного автора!'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='Подсписываться на себя нельзя!'
            )
        ]
        verbose_name='Подписка'
        verbose_name_plural='Подписки'

    def __str__(self):
        return f'{self.user.first_name} подписан на {self.author.first_name}'
