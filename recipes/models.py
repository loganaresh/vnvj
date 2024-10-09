from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField(help_text="Quantity required in the recipe")
    unit = models.CharField(max_length=50, help_text="Unit of measure (e.g., grams, cups)")
    calories = models.FloatField(help_text="Calories per unit", default=0)
    protein = models.FloatField(help_text="Protein per unit in grams", default=0)
    fat = models.FloatField(help_text="Fat per unit in grams", default=0)
    carbs = models.FloatField(help_text="Carbohydrates per unit in grams", default=0)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    preparation_steps = models.TextField()
    cooking_time = models.IntegerField(help_text="Time in minutes")
    categories = models.ManyToManyField(Category)
    tags = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount used in the recipe")

    def __str__(self):
        return f"{self.amount} of {self.ingredient.name} in {self.recipe.title}"


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)  # 1 to 5 scale
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.recipe.title}"
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Meal Plan: {self.title} for {self.user.username}"

class MealPlanRecipe(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    meal_date = models.DateField()

    def __str__(self):
        return f"{self.recipe.title} on {self.meal_date}"

class GroceryList(models.Model):
    meal_plan = models.OneToOneField(MealPlan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_grocery_items(self):
        ingredients = {}
        meal_plan_recipes = MealPlanRecipe.objects.filter(meal_plan=self.meal_plan)
        for meal_plan_recipe in meal_plan_recipes:
            for recipe_ingredient in RecipeIngredient.objects.filter(recipe=meal_plan_recipe.recipe):
                ingredient = recipe_ingredient.ingredient
                if ingredient.name not in ingredients:
                    ingredients[ingredient.name] = recipe_ingredient.amount
                else:
                    ingredients[ingredient.name] += recipe_ingredient.amount
        return ingredients

    def __str__(self):
        return f"Grocery list for {self.meal_plan.title}"
