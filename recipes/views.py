from rest_framework import viewsets, filters,generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe, Review, Tag, NutritionInfo
from .serializers import RecipeSerializer, ReviewSerializer, TagSerializer
from django.shortcuts import render, get_object_or_404
from .models import Recipe, MealPlan, GroceryList, Ingredient
from django.contrib.auth.decorators import login_required
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'ingredients', 'category', 'tags__name'] 

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]  

class RecipeCreateView(generics.CreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RecipeManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
@login_required
def create_meal_plan(request):
    if request.method == 'POST':
        # Get the recipes selected by the user
        recipes = request.POST.getlist('recipes')
        date = request.POST['date']
        meal_plan = MealPlan.objects.create(user=request.user, date=date)
        meal_plan.recipes.set(recipes)
        meal_plan.save()
        return 
    recipes = Recipe.objects.all()
    return 

@login_required
def generate_grocery_list(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id)
    grocery_list = GroceryList.objects.create(user=request.user)
    
    for recipe in meal_plan.recipes.all():
        for ingredient in recipe.ingredients.all():
            grocery_list.items.add(ingredient)

    return 
from .serializers import RecipeSerializer, MealPlanSerializer, GroceryListSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

class GroceryListViewSet(viewsets.ModelViewSet):
    queryset = GroceryList.objects.all()
    serializer_class = GroceryListSerializer