from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from .serializers import (FollowSerializers,
                          TagSerializers,
                          RecipeWriteSerializers,
                          RecipeReadSerializers,
                          RecipeIngredientSerializers)
from recipes.models import Tag, Recipe, RecipeIngredient
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
    pass


class DownloadShoppingCartViewSet(ModelViewSet):
    """."""
    pass


# Избранное
class FavoriteViewSet(ModelViewSet):
    """."""
    pass 


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
