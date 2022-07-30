from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
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
                            ShoppingCart)
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


class DownloadShoppingCartViewSet(ModelViewSet):
    """."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers


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
