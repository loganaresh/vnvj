from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, MealPlanViewSet, GroceryListViewSet,ReviewViewSet, TagViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'tags', TagViewSet)
router.register(r'meal-plans', MealPlanViewSet)
router.register(r'grocery-lists', GroceryListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
