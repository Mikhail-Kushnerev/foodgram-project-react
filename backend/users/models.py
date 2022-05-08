from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey( 
        User, 
        related_name='follower', 
        on_delete=models.CASCADE 
    ) 
    author = models.ForeignKey( 
        User, 
        related_name='following', 
        on_delete=models.CASCADE 
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

    def __str__(self): 
        return f'{self.user} – {self.author}'