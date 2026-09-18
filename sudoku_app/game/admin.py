from django.contrib import admin
from .models import GameScore


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ["player", "difficulty", "score", "time_completed_seconds",
                     "correct_inputs", "total_inputs", "created_at"]
    list_filter = ["difficulty"]
