from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Recipe
from .serializers import *

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)