from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.books.views import BookViewSet, GenresViewSet, RatingsViewSet

router = DefaultRouter(trailing_slash=True)
router.register('genres', GenresViewSet, basename='genres')
router.register('ratings', RatingsViewSet, basename='ratings')
router.register('', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls))
]
