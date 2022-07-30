from django.contrib import admin
from recipes.models import (Tag,
                            Recipe,
                            Follow,
                            Ingredient,
                            RecipeIngredient,
                            ShoppingCart,
                            Favorite)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Follow)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
