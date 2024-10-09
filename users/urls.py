from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from recipes.views import *

router = DefaultRouter()
router.register(r'favorites', FavoriteRecipeViewSet, basename='favorite')
router.register(r'profiles', UserProfileViewSet)
router.register(r'recipes', RecipeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
