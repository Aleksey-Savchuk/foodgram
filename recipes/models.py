# import webcolors

from django.db import models
from users.models import User

# from .validators import validate_hex_color


# Тэги
class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        verbose_name='Название'
    )
    # color_name = models.CharField(
    #     max_length=20,
    #     blank=False,
    #     unique=True,
    #     verbose_name='Цвет тега',
    #     help_text='Введите цвет на английском языке',
    #     # validators=[validate_hex_color]
    # )
    color = models.CharField(
        max_length=7,
        # blank=True,
        verbose_name='Цветовой HEX-код',
        help_text='Не вводите значение, оно введется автоматически',
    )
    slug = models.SlugField(
        blank=False,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     self.color = webcolors.name_to_hex(self.color_name)
    #     super().save(*args, **kwargs)


# Рецепты
class Recipe(models.Model):
    "Модель рецептов"
    author = models.ForeignKey(
        User,
        related_name='reсipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        db_index=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    text = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления в минутах'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes_ingredients',
        verbose_name='Ингредиенты'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['name']

    def __str__(self):
        return self.name


# Список покупок
class ShoppingCart(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='user'
    )
    recipe_cart = models.ForeignKey(
        Recipe,
        verbose_name='Список покупок',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        """."""
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=('user', 'recipe_cart'),
        #         name='unique_shopping_cart'
        #     ),
        #     models.CheckConstraint(
        #         name="prevent_self_shopping_cart",
        #         check=~models.Q(user=models.F("recipe_cart")),
        #     )
        # ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списоки покупок'


# Избранное
class Favorite(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_user'
    )
    favorite = models.ForeignKey(
        Recipe,
        verbose_name='Избранное',
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        """."""
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=('user', 'favorite'),
        #         name='unique_favorite'
        #     ),
        #     models.CheckConstraint(
        #         name="prevent_self_favorite",
        #         check=~models.Q(user=models.F("favorite")),
        #     )
        # ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'


# Подписки
class Follow(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        """."""
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                name="prevent_self_follow",
                check=~models.Q(user=models.F("author")),
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


# Ингридиенты
class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=10,
        blank=False,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredients'
            )
        ]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель привязанная к рецепту и ингридиентам"""
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipes_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='igredients_recipes'
    )
    amount = models.IntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
