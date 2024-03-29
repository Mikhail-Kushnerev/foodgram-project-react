# Продуктовый помощник

Досупен по [ссылке](http://51.250.104.248/recipes)

<details>
  <summary> Админка </summary>

```py
email: muxa@yandex.ru
password: muxa
```

</details>

## Оглавление

- [Технологии](#технологии)
- [Описание](#описание)
- <a href="#structure"> Установка </a>
- [Автор](#автор)

## Технологии

- Python;
- Django-Rest-Framework;
- Recat;
- Gunicorn;
- Docker/Docker-compose;
- Nginx;
- Yandex.Cloud.

[⬆️Оглавление](#оглавление)

## Описание

 Онлайн-сервис, где пользователи могут:

- публиковать рецепты;
- подписываться на публикации других пользователей;
- добавлять понравившиеся рецепты в список «Избранное»;
- перед походом в магазин скачивать сводный список продуктов.

[⬆️Оглавление](#оглавление)

<details>
  <summary>
    <h2 id="structure"> Установка </h2>
  </summary>

### Структура проекта:

```cmd
|   .env
|   .gitignore
|   README.md
|   
+---backend  <--
|   |   Dockerfile
|   |   manage.py
|   |   requirements.txt
|   |   
|   +---api
|   |   |   apps.py
|   |   |   filters.py
|   |   |   pagination.py
|   |   |   permissions.py
|   |   |   urls.py
|   |   |   utils.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   +---backend
|   |   |   asgi.py
|   |   |   settings.py
|   |   |   urls.py
|   |   |   wsgi.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   +---data  <-- Данные для наполнения БД "Ингредиенты"
|   |       ingredients.csv
|   |       ingredients.json
|   |       
|   +---recipes
|   |   |   admin.py
|   |   |   apps.py
|   |   |   models.py
|   |   |   serializers.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |           
|   |   \---__pycache__
|   |           
|   +---scripts  <-- Скрипт для заполнения БД "Ингредиенты"
|   |   |   load_ing_data.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   \---users
|       |   admin.py
|       |   apps.py
|       |   models.py
|       |   serializers.py
|       |   views.py
|       |   __init__.py
|       |   
|       \---__pycache__
|               
+---docs  <-- Документация по API
|       openapi-schema.yml
|       redoc.html
|       
+---frontend  <-- Фронтенд для сборки файлов
|   |   Dockerfile
|   |   package-lock.json
|   |   package.json
|   |   yarn.lock
|   |   
|   ...
|         
+---infra  <-- Сборка контейнеров, настройка сервера
|       docker-compose.yml
|       nginx.conf
|       
\---venv
```

- Склонируйте репозиторий на свой компьютер:

```py
https://github.com/Mikhail-Kushnerev/foodgram-project-react/
```

- Соберите контейнеры из папки `infra`:

```py
docker-compose up -d
```

- В контейнере **backend**:
    - выполните миграции;
    - установите **superuser**;
    - заполните БД исходными данными:

```py
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py runscript load_ing_data
```

[⬆️Оглавление](#оглавление)

</details>

## Автор

[Mikhail Kushnerev](https://github.com/Mikhail-Kushnerev)  
[⬆️В начало](#оглавление)
