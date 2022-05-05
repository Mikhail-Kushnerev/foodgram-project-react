import csv

from recipes.models import Ingredient


def run():
    with open('../data/ingredients.csv', encoding='utf-8') as file:
        reader = csv.reader(file)

        for value in reader:
            Ingredient.objects.create(
                name=value[0],
                measurement_unit=value[1]
            )
