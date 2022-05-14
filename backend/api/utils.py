from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe

from .serializers import RecipeUser


def download_page(cart_list):
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
    for i, (name, data) in enumerate(cart_list, 1):
        page.drawString(75, height, (
            f'{i}. {name}: {data["amount"]}, '
            f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return response


def add_or_delete(request, model, obj_id):
    user = request.user
    if request.method == 'DELETE':
        obj = model.objects.filter(
            user=user,
            recipe__id=obj_id
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    if model.objects.filter(
        user=user,
        recipe__id=obj_id
    ).exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(
        Recipe,
        id=obj_id
    )
    model.objects.create(
        user=user,
        recipe=recipe
    )
    serializer = RecipeUser(recipe)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )
