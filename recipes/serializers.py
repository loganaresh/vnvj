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
    created_by = serializers.ReadOnlyField(source='created_by.username')  # To show the creator's name

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'created_by', 'tags']  # Include all fields you want
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
