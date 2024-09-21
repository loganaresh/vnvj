from rest_framework import serializers
from .models import Recipe, Review, Tag, NutritionInfo

class NutritionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionInfo
        fields = ['calories', 'protein', 'fat', 'carbohydrates']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'comment', 'created_at']

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
