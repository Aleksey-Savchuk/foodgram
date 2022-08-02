from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef, Sum, Q, Count, ExpressionWrapper
from django.db.models import IntegerField
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.response import Response
from .serializers import (FollowSerializers,
                          TagSerializers,
                          RecipeWriteSerializers,
                          RecipeReadSerializers,
                          RecipeIngredientSerializers,
                          FavoriteSerializers,
                          ShoppingCartSerializers)
from recipes.models import (Tag,
                            Recipe,
                            RecipeIngredient,
                            Favorite,
                            ShoppingCart,
                            Ingredient)
from users.models import User
from rest_framework.pagination import PageNumberPagination


# Тэги
class TagViewSet(ModelViewSet):
    """."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


# Рецепты
class RecipeViewSet(ModelViewSet):
    """."""
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializers
        return RecipeWriteSerializers


# Список покупок
class ShoppingCartViewSet(ModelViewSet):
    """."""
    serializer_class = ShoppingCartSerializers

    def get_shopping_cart(self):
        """FollowViewSet_get_follow."""
        return get_object_or_404(
            Recipe,
            pk=self.kwargs.get('shopping_cart_id'),
            )

    def get_queryset(self):
        """FollowViewSet_get_queryset."""
        return self.get_shopping_cart().recipe_cart.all()

    def perform_create(self, serializer):
        """FollowViewSet_perform_create."""
        return serializer.save(
            user=self.request.user,
            recipe_cart=self.get_shopping_cart())


class DownloadShoppingCartViewSet(APIView):
    """."""
    def get(self, request):
        sq_use = Q(user=self.request.user)
        sq = ShoppingCart.objects.filter(sq_use).values_list('recipe_cart_id')
        q_sq = Q(igredients_recipes__recipe__in=sq)
        ing = Ingredient.objects.annotate(
            sum=Sum('igredients_recipes__amount',
                    output_field=IntegerField(),
                    filter=q_sq)).filter(sum__gt=0).values('name',
                                                           'measurement_unit',
                                                           'sum')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('DejaVuSerif',
                                       'DejaVuSerif.ttf',
                                       'UTF-8'))
        p.setFont("DejaVuSerif", 18)
        p.drawString(25, 800, "№ пп")
        p.drawString(125, 800, "Наименование")
        p.drawString(400, 800, "ед. из.")
        p.drawString(525, 800, "Кол-во")
        n = 1
        p_str = 775
        for k in ing:
            p.drawString(25, p_str, str(n))
            p.drawString(125, p_str, str(k['name']))
            p.drawString(400, p_str, str(k['measurement_unit']))
            p.drawString(525, p_str, str(k['sum']))
            n += 1
            p_str -= 25
        p.showPage()
        p.save()
        return response


# Избранное
class FavoriteViewSet(ModelViewSet):
    """."""
    serializer_class = FavoriteSerializers

    def get_shopping_cart(self):
        """FollowViewSet_get_follow."""
        return get_object_or_404(
            Recipe,
            pk=self.kwargs.get('favorite_id'),
            )

    def get_queryset(self):
        """FollowViewSet_get_queryset."""
        return self.get_shopping_cart().recipe_cart.all()

    def perform_create(self, serializer):
        """FollowViewSet_perform_create."""
        return serializer.save(
            user=self.request.user,
            favorite=self.get_shopping_cart())


# Подписки
class FollowViewSet(ModelViewSet):
    """FollowViewSet."""

    serializer_class = FollowSerializers

    def get_follow(self):
        """FollowViewSet_get_follow."""
        return get_object_or_404(
            User,
            pk=self.kwargs.get('author_id'),
            )

    def get_queryset(self):
        """FollowViewSet_get_queryset."""
        return self.get_follow().author.all()

    def perform_create(self, serializer):
        """FollowViewSet_perform_create."""
        return serializer.save(
            user=self.request.user,
            author=self.get_follow())


# Ингридиенты
class RecipeIngredientViewSet(ModelViewSet):
    """."""
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializers
    pagination_class = PageNumberPagination
