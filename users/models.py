from django.db import models
from django.conf import settings
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    def __str__(self):
        return self.user.username
class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorited_by")
