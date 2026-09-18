from rest_framework import mixins, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import GameScore
from .serializers import GameScoreReadSerializer, GameScoreSubmitSerializer
from .sudoku_logic import generate_puzzle, DIFFICULTY_CLUES


@api_view(["GET"])
def get_puzzle(request, difficulty):
    difficulty = difficulty.lower()
    if difficulty not in DIFFICULTY_CLUES:
        raise ValidationError("difficulty must be one of: easy, medium, hard")

    puzzle, solution = generate_puzzle(difficulty)
    return Response({
        "difficulty": difficulty,
        "puzzle": puzzle,
        "solution": solution,
    })


class GameScoreViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = GameScore.objects.select_related("player").all()

    def get_serializer_class(self):
        if self.action == "create":
            return GameScoreSubmitSerializer
        return GameScoreReadSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        player_id = self.request.query_params.get("player")
        if player_id:
            qs = qs.filter(player_id=player_id)
        return qs

    def create(self, request, *args, **kwargs):
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        read_serializer = GameScoreReadSerializer(instance)
        return Response(read_serializer.data, status=201)


class LeaderboardView(generics.ListAPIView):
    """Top scores, optionally filtered by ?difficulty=easy|medium|hard."""
    serializer_class = GameScoreReadSerializer

    def get_queryset(self):
        qs = GameScore.objects.select_related("player").order_by("-score")
        difficulty = self.request.query_params.get("difficulty")
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return qs[:20]
