from django.contrib import admin

from apps.books.models import Book, Genre, Author, Favorite, Rating


class BookAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description', 'publication_date')
    fields = ('uuid', 'genre', 'author', 'name', 'description', 'publication_date')
    readonly_fields = ('uuid', )


class GenreAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    readonly_fields = ('uuid', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    readonly_fields = ('uuid', )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'book', 'user')
    readonly_fields = ('uuid', )


class RatingAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'book', 'user', 'feedback', 'rated_on', 'value')
    readonly_fields = ('uuid', )


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Rating, RatingAdmin)
