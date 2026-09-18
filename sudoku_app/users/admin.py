# Backend/sudoku_app/users/admin.py
from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "age", "gender", "high_score", "created_at"]
    search_fields = ["name"]
