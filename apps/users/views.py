from django.contrib.auth import get_user_model
from rest_framework import viewsets

from apps.authentication.serializers import UserRegistrationSerializer
from apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializers(self):
        serializers = {
            'create': UserRegistrationSerializer
        }
        return serializers

    def get_serializer_class(self):
        serializers = {**self.get_serializers()}
        if self.action in serializers:
            if serializer := serializers[self.action]:
                return serializer
        return self.serializer_class
