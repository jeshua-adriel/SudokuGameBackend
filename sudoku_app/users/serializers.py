from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        trim_whitespace=False,
    )

    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "email",
            "password",
            "age",
            "gender",
            "high_score",
            "created_at",
        ]

    def create(self, validated_data):
        raw_password = validated_data.pop("password", "")
        player = Player(**validated_data)
        player.set_password(raw_password)
        player.save()
        return player