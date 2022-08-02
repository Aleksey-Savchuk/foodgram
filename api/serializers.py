from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import (Follow,
                            Tag,
                            Recipe,
                            Ingredient,
                            User,
                            RecipeIngredient,
                            ShoppingCart,
                            Favorite)


# Тэги
class TagSerializers(serializers.ModelSerializer):
    class Meta:
        """."""
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class TagsMethod(serializers.Field):
    """."""
    def to_representation(self, value):
        """."""
        serializer = TagSerializers(value, many=True)
        return serializer.data

    def to_internal_value(self, data):
        """."""
        return data


# Рецепты
class IngridientSerializers(serializers.ModelSerializer):
    """."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializers(serializers.ModelSerializer):
    """."""
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class AuthorSerializers(serializers.ModelSerializer):
    """."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """."""
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if Follow.objects.filter(user=request.user.pk,
                                 author=obj.id).count() > 0:
            return True
        return False


class RecipeReadSerializers(serializers.ModelSerializer):
    author = AuthorSerializers(read_only=True)
    # ingredients = IngridientSerializers(read_only=True,
    #                                     many=True,
    #                                     source='recipes_ingredients')
    tags = TagsMethod()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        """."""
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                #   'ingredients',
                  'name',
                  'text',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context['request']
        if Favorite.objects.filter(user=request.user.pk, favorite=obj.pk).count() > 0:
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if ShoppingCart.objects.filter(user=request.user.pk, recipe_cart=obj.pk).count() > 0:
            return True
        return False


class RecipeWriteSerializers(serializers.ModelSerializer):
    pass
#     tags = TagsMethod()
    # ingredients = IngridientSerializers(read_only=True,
    #                                     many=True,
    #                                     source='recipes_ingredients')

    # class Meta:
    #     """."""
    #     model = Recipe
    #     fields = ('ingredients',
    #               'author',
    #               'tags',
    #               'name',
    #               'text',
    #               'cooking_time'
    #               )

    # def create(self, validated_data):
    #     """."""
    #     ingridients = validated_data.pop('ingridients')

    #     recipe = Recipe.objects.create(**validated_data)
    #     for ing in ingridients:
    #         curent_ing, status = RecipeIngredient.objects.get_or_create(**ing)
    #         Ingredient.objects.create(ing=curent_ing.id,
    #                                   recipe=recipe,
    #                                   amount=curent_ing.amount)
    #     return recipe


# Список покупок
class ShoppingCartSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='pk')

    class Meta:
        """."""
        model = ShoppingCart
        fields = ('__all__')
        read_only_fields = ('user', 'recipe_cart')


# Избранное
class FavoriteSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='pk')

    class Meta:
        """."""
        model = Favorite
        fields = ('__all__')
        read_only_fields = ('user', 'favorite')


# Подписки
class FollowSerializers(serializers.ModelSerializer):
    """."""
    user = serializers.SlugRelatedField(read_only=True, slug_field='pk')

    class Meta:
        """."""
        model = Follow
        fields = ('__all__')
        read_only_fields = ('author',)


# Ингридиенты




class EmailSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" как юзернейм запрещено'
            )
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Юзернейм не уникален'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Email не уникален'
            )
        return data

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
