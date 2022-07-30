from rest_framework import serializers
from recipes.models import (Follow,
                            Tag,
                            Recipe,
                            Ingredient,
                            User,
                            RecipeIngredient)


# Тэги
class TagSerializers(serializers.ModelSerializer):
    class Meta:
        """."""
        model = Tag
        fields = ('__all__')


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
    class Meta:
        """."""
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class RecipeReadSerializers(serializers.ModelSerializer):
    author = AuthorSerializers(read_only=True)
    ingredients = IngridientSerializers(read_only=True,
                                        many=True,
                                        source='recipes_ingredients')
    tags = TagsMethod()

    class Meta:
        """."""
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                #   'image',
                  'text',
                  'cooking_time')


class RecipeWriteSerializers(serializers.ModelSerializer):
    tags = TagsMethod()
    ingredients = IngridientSerializers(read_only=True,
                                        many=True,
                                        source='recipes_ingredients')

    class Meta:
        """."""
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                # 'image',
                  'text',
                  'cooking_time')

    def create(self, validated_data):
        """."""
        ingridients = validated_data.pop('ingridients')

        recipe = Recipe.objects.create(**validated_data)
        for ingridient in ingridients:
            curent_ingridient, status = RecipeIngredient.objects.get_or_create(**ingridient)
            Ingredient.objects.create(ingridient=curent_ingridient.id,
                                      recipe=recipe,
                                      amount=curent_ingridient.amount)
        return recipe


class FollowSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='pk')

    class Meta:
        """."""
        model = Follow
        fields = ('__all__')
        read_only_fields = ('author',)