from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from users.serializers.user_self import ChangePasswordSerializer
from users.permissions import IsAuthenticatedUserSelf


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticatedUserSelf]

    @extend_schema(
        tags=['user-self'],
        summary='Смена пароля пользователя',
        description='Позволяет залогиненному пользователю изменить пароль, указав старый и новый',
        request=ChangePasswordSerializer,
        responses={200: None}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)
