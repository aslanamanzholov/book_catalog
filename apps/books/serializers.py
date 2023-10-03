from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.books.models import Book, Genre, Rating, Author
from apps.users.serializers import UserSerializer


# Genre Serializers
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('uuid', 'name',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('uuid', 'name',)


# Rating Serializers
class RatingsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ('uuid', 'book', 'user', 'feedback', 'rated_on', 'value')

    def validate(self, attrs):
        value = attrs.get('value')
        if value > 10:
            raise ValidationError(detail='Максимально допустимая оценка книге - 10')
        return attrs


class RatingsMainInformationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = ('uuid', 'user', 'feedback', 'rated_on', 'value')


# Book Serializers
class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source='get_rating')
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('uuid', 'name', 'genre', 'author', 'rating', 'publication_date', 'is_favorite')

    def get_is_favorite(self, obj):
        """
        Getter boolean field from model Favorite
        """
        request = self.context.get('request', None)
        if obj.favorite.filter(user_id=request.user.uuid).exists():
            return True
        return False


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('uuid', 'genre', 'author', 'name', 'description', 'publication_date')


class BookRetrieveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source='get_rating')
    reviews_list = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('uuid', 'genre', 'author', 'name', 'description', 'publication_date', 'rating',
                  'reviews_list', 'created_at')

    def get_reviews_list(self, obj):
        return RatingsMainInformationSerializer(obj.ratings.all(), many=True).data
