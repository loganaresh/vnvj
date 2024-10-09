from rest_framework import serializers
from .models import Recipe, Category, Review , Ingredient, RecipeIngredient, MealPlan, MealPlanRecipe, GroceryList
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import serializers

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity', 'unit', 'calories', 'protein', 'fat', 'carbs']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'preparation_steps', 'cooking_time', 'tags']
        ref_name = 'CustomRecipeSerializer'
class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['id', 'title', 'start_date', 'end_date']

class MealPlanRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()

    class Meta:
        model = MealPlanRecipe
        fields = ['meal_plan', 'recipe', 'meal_date']

class GroceryListSerializer(serializers.ModelSerializer):
    grocery_items = serializers.SerializerMethodField()

    class Meta:
        model = GroceryList
        fields = ['meal_plan', 'grocery_items']

    def get_grocery_items(self, obj):
        return obj.get_grocery_items()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'preparation_steps', 'cooking_time', 'categories', 'tags', 'created_by']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'rating', 'review_text', 'user', 'created_at']
