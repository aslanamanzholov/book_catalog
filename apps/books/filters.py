import django_filters

from apps.books.models import Book


class BookFilterSet(django_filters.FilterSet):
    publication_date__begin = django_filters.IsoDateTimeFilter(field_name="publication_date", lookup_expr="gte")
    publication_date__end = django_filters.IsoDateTimeFilter(field_name="publication_date", lookup_expr="lte")

    ordering = django_filters.OrderingFilter(
        fields=(
            ("author", "author"),
            ("name", "name"),
            ("publication_date", "publication_date"),
        )
    )

    class Meta:
        model = Book
        fields = (
            'name', 'author', 'genre', 'publication_date__begin', 'publication_date__end',
        )
