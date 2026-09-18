from django.db import models
from users.models import Player


class GameScore(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    player = models.ForeignKey(Player, related_name="scores", on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    time_completed_seconds = models.PositiveIntegerField()
    correct_inputs = models.PositiveIntegerField()
    total_inputs = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.player.name} - {self.difficulty} - {self.score}"
