from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import viewsets, status

from apps.authentication.serializers import AuthTokenSerializer, UserRegistrationWithEmailSerializer
from apps.authentication.tokens import account_activation_token

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserRegisterWithEmailValidate(CreateAPIView):
    """
    A viewset for register user instance.
    """
    serializer_class = UserRegistrationWithEmailSerializer
    queryset = User.objects.all()
    lookup_field = 'uuid'


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return Response({'detail': 'Ваш аккаунт активирован'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Ссылка недеиствительна'}, status=status.HTTP_200_OK)
