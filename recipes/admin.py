from django.contrib import admin
from users.models import User
from recipes.models import (Tag,
                            Recipe,
                            Follow,
                            Ingredient,
                            RecipeIngredient,
                            ShoppingCart,
                            Favorite)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'username',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time',

    )
    list_filter = ('author',
                   'name',
                   'tags',
                   )
    readonly_fields = ('count_favorite',)       
    empty_value_display = '-пусто-'

    def count_favorite(self, rec):
        return Favorite.objects.filter(favorite=rec.id).count()
    count_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'user',
        'recipe_cart'
    )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'user',
        'favorite'
    )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'user',
        'author'
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """."""
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount'
    )
    empty_value_display = '-пусто-'
