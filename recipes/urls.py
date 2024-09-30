from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, MealPlanViewSet, GroceryListViewSet,ReviewViewSet, TagViewSet,RecipeListView, RecipeCreateView, RecipeManageView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'tags', TagViewSet)
router.register(r'meal-plans', MealPlanViewSet)
router.register(r'grocery-lists', GroceryListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
