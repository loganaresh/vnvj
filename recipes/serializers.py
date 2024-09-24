from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_at']
class NutritionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionInfo
        fields = ['calories', 'protein', 'fat', 'carbohydrates']


class RecipeSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    nutrition_info = NutritionInfoSerializer(read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'preparation_steps', 'cooking_time', 'category', 'tags', 'reviews', 'nutrition_info', 'created_by']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

class MealPlanSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True)

    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'date', 'recipes']

class GroceryListSerializer(serializers.ModelSerializer):
    items = IngredientSerializer(many=True)

    class Meta:
        model = GroceryList
        fields = ['id', 'user', 'items', 'created_at']

