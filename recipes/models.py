from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()  # Ingredients can be stored as text or JSON
    preparation_steps = models.TextField()  # Step-by-step instructions
    cooking_time = models.IntegerField()  # In minutes
    category = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag', related_name='recipes')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.recipe.title} - {self.user.username}'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class NutritionInfo(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    calories = models.IntegerField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrates = models.FloatField()

    def __str__(self):
        return f'Nutrition info for {self.recipe.title}'
