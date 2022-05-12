import webcolors
from django.contrib import admin
from django.http import HttpResponse
from recipes.models import Recipe
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import serializers


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class RecipeUser(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class IngredientFilter(admin.SimpleListFilter):

    title = 'Ингредиенты'
    parameter_name = 'ингредиенты_категории'

    def lookups(self, request, model_admin):
        pattern = 'абвгдеёжзийклмнопрстуфхцчшщэюя'
        return [(i, i) for i in pattern]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(name__startswith=self.value())
        return queryset


def download_page(unit_sum_dict):
    pdfmetrics.registerFont(
        TTFont('DejaVuSans', 'DejaVuSans.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )
    page = canvas.Canvas(response)
    page.setFont('DejaVuSans', size=24)
    page.drawString(200, 800, 'Список покупок')
    page.setFont('DejaVuSans', size=16)
    height = 750
    for i, (name, data) in enumerate(unit_sum_dict.items(), 1):
        page.drawString(75, height, (
            f'{i}. {name}: {data["amount"]}, '
            f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return response
