from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, MealPlanViewSet, GroceryListViewSet,ReviewViewSet, TagViewSet,RecipeListView, RecipeCreateView, RecipeManageView
schema_view = get_schema_view(
    openapi.Info(
        title="Recipe API",
        default_version='v1',
        description="API documentation for Recipe management",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'tags', TagViewSet)
router.register(r'meal-plans', MealPlanViewSet)
router.register(r'grocery-lists', GroceryListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/', RecipeManageView.as_view(), name='recipe-manage'),
]
