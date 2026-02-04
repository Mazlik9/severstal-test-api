from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from users.serializers import UserLogoutSerializer
from rest_framework.permissions import IsAuthenticated


@extend_schema(
    tags=['user'],
    summary='Logout пользователя',
    description='Добавление refresh токена в черный список (logout)'
)
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Успешный logout"}, status=status.HTTP_204_NO_CONTENT)
