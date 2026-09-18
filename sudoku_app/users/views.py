from django.core import signing
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Player
from .serializers import PlayerSerializer


TOKEN_SALT = "sudoku-player-auth"
TOKEN_MAX_AGE = 60 * 60 * 24


def create_access_token(player):
    return signing.dumps({"player_id": player.id}, salt=TOKEN_SALT)


class CreatePlayerAPIView(generics.CreateAPIView):
    queryset = Player.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PlayerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.save()
        return Response(
            {
                "access": create_access_token(player),
                "username": player.name,
                "player": PlayerSerializer(player).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        name = (request.data.get("name") or request.data.get("username") or "").strip()
        password = request.data.get("password")

        if not name or password is None:
            return Response(
                {"detail": "Name and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            player = Player.objects.get(name=name)
        except Player.DoesNotExist:
            return Response(
                {"detail": "Invalid name or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not player.check_password(password):
            return Response(
                {"detail": "Invalid name or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "access": create_access_token(player),
                "username": player.name,
                "player": PlayerSerializer(player).data,
            },
            status=status.HTTP_200_OK,
        )


class PlayerDetailAPIView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PlayerSerializer


class CurrentPlayerAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return Response({"detail": "Authentication credentials were not provided."}, status=401)

        try:
            payload = signing.loads(
                header.removeprefix("Bearer ").strip(),
                salt=TOKEN_SALT,
                max_age=TOKEN_MAX_AGE,
            )
            player = Player.objects.get(id=payload["player_id"])
        except (KeyError, Player.DoesNotExist, signing.BadSignature, signing.SignatureExpired):
            return Response({"detail": "Invalid or expired authentication token."}, status=401)

        return Response(PlayerSerializer(player).data)