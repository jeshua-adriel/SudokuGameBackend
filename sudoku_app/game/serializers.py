from rest_framework import serializers
from .models import GameScore
from .scoring import compute_score


class GameScoreReadSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.name", read_only=True)

    class Meta:
        model = GameScore
        fields = [
            "id", "player", "player_name", "difficulty",
            "time_completed_seconds", "correct_inputs", "total_inputs",
            "score", "created_at",
        ]


class GameScoreSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScore
        fields = [
            "id", "player", "difficulty",
            "time_completed_seconds", "correct_inputs", "total_inputs",
            "score", "created_at",
        ]
        read_only_fields = ["id", "score", "created_at"]

    def validate(self, data):
        if data["correct_inputs"] > data["total_inputs"]:
            raise serializers.ValidationError(
                "correct_inputs can't exceed total_inputs."
            )
        return data

    def create(self, validated_data):
        validated_data["score"] = compute_score(
            difficulty=validated_data["difficulty"],
            time_completed_seconds=validated_data["time_completed_seconds"],
            correct_inputs=validated_data["correct_inputs"],
            total_inputs=validated_data["total_inputs"],
        )
        instance = super().create(validated_data)

        player = instance.player
        if instance.score > player.high_score:
            player.high_score = instance.score
            player.save(update_fields=["high_score"])

        return instance
