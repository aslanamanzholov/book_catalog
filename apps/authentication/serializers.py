from smtplib import SMTPServerDisconnected

from django.contrib.auth import authenticate, get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.response import Response

from apps.authentication.tokens import account_activation_token

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'email', 'password', 'first_name', 'last_name')


class UserRegistrationWithEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        email = validated_data.get('email')
        instance = User.objects.create_user(**validated_data)
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        email_subject = 'Подтверждение email'
        message = {
            'user': instance,
            'domain': 'localhost',
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)).encode().decode('utf-8'),
            'token': account_activation_token.make_token(instance),
        }
        email = EmailMessage(email_subject, message, to=[email])
        email.send()
        return Response({'detail': 'Пожалуйста подтвердите вашу почту для регистраций'})
