from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from account import models, serializers, permissions
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from account.utils import send_reset_email


class UserViewSets(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.UpdateOwnProfile,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id',)
    search_fields = ('username', 'email',)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = f"User with name {instance.username} has been deleted."
        return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = Token.objects.get(key=response.data['token']).user
            user.last_login = timezone.now()
            user.save()

        return response


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()

        return Response({'detail': 'Logged out successfully.'})


class ForgotPasswordView(APIView):

    def post(self, request, format=None):
        serializer = serializers.ForgotPasswordSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = models.UserProfile.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            encoded_token = urlsafe_base64_encode(force_bytes(token.key))
            data = send_reset_email(email, encoded_token, user.username)
            if data.get('is_sent'):
                return Response({'message': "Reset link is sent to your email"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': data.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordConfirmView(APIView):
    @staticmethod
    def get_user_from_encoded_token(token):
        try:
            decoded_token = force_str(urlsafe_base64_decode(token))
            token_obj = Token.objects.get(key=decoded_token)
            user = token_obj.user
            return user
        except Exception:
            return None

    def post(self, request, token):
        serializer = serializers.ForgotPasswordConfirmSerializers(data=request.data)

        if serializer.is_valid():

            user = self.get_user_from_encoded_token(token)

            if user is not None:
                user.set_password(serializer.validated_data.get('password'))
                user.save()
                return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
