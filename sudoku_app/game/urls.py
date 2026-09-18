from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import get_puzzle, GameScoreViewSet, LeaderboardView

router = DefaultRouter()
router.register(r"scores", GameScoreViewSet, basename="score")

urlpatterns = [
    path("puzzle/<str:difficulty>/", get_puzzle, name="get-puzzle"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
] + router.urls
