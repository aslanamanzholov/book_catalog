from django.urls import path

from apps.authentication import views
from apps.authentication.views import CustomAuthToken, UserRegisterWithEmailValidate

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('create_user_for_activate/', UserRegisterWithEmailValidate.as_view()),
    path('activate/(<uidb64>/<token>/', views.activate_account),
]
