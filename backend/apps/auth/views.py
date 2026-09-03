

from rest_framework import status
# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.services.jwt_service import ActivateToken, JWTService, SocketToken

from apps.user.serializers import UserSerializer


class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken) #виклик метода для перевірки токена
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

class SocketTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def get(self, *args, **kwargs):

     token = JWTService.create_token(user=self.request.user, token_class=SocketToken)
     return Response({'token': str(token)}, status.HTTP_200_OK)