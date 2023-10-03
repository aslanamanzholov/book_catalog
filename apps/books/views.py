from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.books.filters import BookFilterSet
from apps.books.models import Book, Genre, Rating
from apps.books.serializers import (BookListSerializer, BookCreateSerializer,
                                    BookRetrieveSerializer, GenreSerializer, RatingsSerializer, )


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    """
    serializer_class = BookListSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilterSet

    def get_serializers(self):
        serializers = {
            'retrieve': BookRetrieveSerializer,
            'create': BookCreateSerializer
        }
        return serializers

    def get_serializer_class(self):
        serializers = {**self.get_serializers()}
        if self.action in serializers:
            if serializer := serializers[self.action]:
                return serializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='add-favorite')
    def add_favorite(self, request, uuid, *args, **kwargs):
        """
        API for add/delete book to/from favorite
        """
        book = self.get_object()
        user = request.user
        if not user.favorite_books.all().exists():
            user.favorite_books.add(book)
        else:
            user.favorite_books.remove(book)
        return Response({'success': True}, status=status.HTTP_200_OK)


class GenresViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing genre instances.
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class RatingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing rating instances.
    """
    serializer_class = RatingsSerializer
    queryset = Rating.objects.all()
