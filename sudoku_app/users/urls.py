# Backend/sudoku_app/users/urls.py
from django.urls import path
from .views import (
    CreatePlayerAPIView,
    CurrentPlayerAPIView,
    CustomLoginAPIView,
    PlayerDetailAPIView,
)

urlpatterns = [
    path('register/', CreatePlayerAPIView.as_view(), name='api_register'),
    path('login/', CustomLoginAPIView.as_view(), name='api_login'),
    path('me/', CurrentPlayerAPIView.as_view(), name='api_current_player'),
    path('<int:pk>/', PlayerDetailAPIView.as_view(), name='api_player_detail'),
]
