from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'favorites', FavoriteRecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
