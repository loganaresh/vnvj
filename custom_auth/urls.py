from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name="register"),
    path('update/', views.update_view, name="update"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('refresh/', views.refresh_view, name="refresh")
]

