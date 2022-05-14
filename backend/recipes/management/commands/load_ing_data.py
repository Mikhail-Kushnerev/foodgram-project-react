import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

DIR = os.path.join(settings.BASE_DIR, 'data')
FILE_NAME = 'ingredients.json'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            default=FILE_NAME,
            nargs='?',
            type=str
        )

    def handle(self, *args, **options):
        file_path = os.path.join(DIR, options['file'])
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for ingredient in data:
                Ingredient.objects.update_or_create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit'])
