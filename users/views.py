from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, Count
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from recipes.models import *
from recipes.serializers import *

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    

class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
@api_view(['GET'])
def get_search_history(request):
    user = request.user
    search_history = UserSearchHistory.objects.filter(user=user).order_by('-timestamp')[:10]  # Last 10 searches
    history_data = [{'keyword': history.keyword, 'timestamp': history.timestamp} for history in search_history]
    return Response(history_data)

   
@api_view(['GET'])
def search_recipes(request):
    query = request.GET.get('q', '')
    user = request.user
    if query:
        UserSearchHistory.objects.create(user=user, keyword=query)
    search_results = Recipe.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    serializer = RecipeSerializer(search_results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recommend_recipes(request):
    user = request.user
    user_favorites = user.favorites.values_list('recipe', flat=True)
    search_keywords = UserSearchHistory.objects.filter(user=user).values_list('keyword', flat=True)
    trending_recipes = Recipe.objects.annotate(num_favorites=Count('favorites')).order_by('-num_favorites')[:5]
    recommendations = Recipe.objects.exclude(id__in=user_favorites)
    if search_keywords.exists():
        recommendations = recommendations.filter(title__icontains=search_keywords[0])[:5]
    else:
        recommendations = recommendations.order_by('?')[:5]
    recommendations = list(recommendations) + list(trending_recipes)
    serializer = RecipeSerializer(recommendations, many=True)
    return Response(serializer.data)