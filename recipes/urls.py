from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, ReviewViewSet, TagViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
