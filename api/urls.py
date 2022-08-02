"""api_urls."""
from django.urls import include, path
from rest_framework import routers

from .views import (FollowViewSet,
                    TagViewSet,
                    RecipeViewSet,
                    RecipeIngredientViewSet,
                    ShoppingCartViewSet,
                    DownloadShoppingCartViewSet,
                    FavoriteViewSet)

router = routers.DefaultRouter()

# Тэги
    # GET api/tags/
    # GET api/tags/{id}/
router.register(
    r'tags',
    TagViewSet, basename='tags')

# Рецепты
    # GET api/recipes/
    # POST api/recipes/
    # GET api/recipes/{id}/
    # PATCH api/recipes/{id}/
    # DEL api/recipes/{id}/
router.register(
    r'recipes',
    RecipeViewSet, basename='recipes')

# Список покупок
    # GET api/recipes/download_shopping_cart/
    # POST api/recipes/{id}/shopping_cart/
    # DEL api/recipes/{id}/shopping_cart/
# router.register(
#     r'recipes/download_shopping_cart/',
#     DownloadShoppingCartViewSet, basename='download_shopping_cart')
router.register(
    r'recipes/(?P<shopping_cart_id>\d+)/shopping_cart',
    ShoppingCartViewSet, basename='shopping_cart')

# Избранное
    # POST api/recipes/{id}/favorite/
    # DEL api/recipes/{id}/favorite/
router.register(
    r'recipes/(?P<favorite_id>\d+)/favorite',
    FavoriteViewSet, basename='favorite')


# Подписки
    # GET api/users/subscriptions/
    # POST api/users/{id}/subscribe/
    # DEL api/users/{id}/subscribe/
router.register(
    r'users/(?P<author_id>\d+)/subscribe',
    FollowViewSet, basename='follow')

# Ингридиенты
    # GET api/ingredients/
    # GET api/ingredients/{id}/

router.register(
    r'ingredients',
    RecipeIngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)),
    # path('user/<int:pk>/', FollowViewSet.as_view())
    path('recipes/download_shopping_cart/25/',
         DownloadShoppingCartViewSet.as_view())
    # path('v1/auth/signup/', send_confirmation_code, name='singup'),
    # path('v1/auth/token/', send_auth_token, name='token'),
]
