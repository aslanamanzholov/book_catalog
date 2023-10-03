from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.common.models import UUIDModel, TimestampMixin


class Book(UUIDModel, TimestampMixin):
    genre = models.ManyToManyField(
        verbose_name=_('Жанр'),
        to='books.Genre',
        related_name='books',
        blank=False
    )
    author = models.ManyToManyField(
        verbose_name=_('Автор'),
        to='books.Author',
        related_name='books'
    )
    name = models.CharField(verbose_name=_("Название книги"), max_length=255, blank=True, null=True)
    description = models.CharField(verbose_name=_("Описание книги"), max_length=255, blank=True, null=True)
    publication_date = models.DateField(verbose_name=_("Дата публикаций"), blank=True, null=True)

    class Meta:
        verbose_name = _("Книга")
        verbose_name_plural = _("Книги")

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def get_rating(self):
        return self.ratings.all().aggregate(Avg('value'))['value__avg'] if self.ratings.all().exists() else 0


class Genre(UUIDModel, TimestampMixin):
    name = models.CharField(verbose_name=_("Название жанра"), max_length=255)

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")

    def __str__(self) -> str:
        return f"{self.name}"


class Author(UUIDModel, TimestampMixin):
    name = models.CharField(verbose_name=_("Автор книги"), max_length=255)

    class Meta:
        verbose_name = _("Автор")
        verbose_name_plural = _("Авторы")

    def __str__(self) -> str:
        return f"{self.name}"


class Favorite(UUIDModel, TimestampMixin):
    book = models.ForeignKey(
        to='books.Book',
        on_delete=models.CASCADE,
        verbose_name=_('Книга'),
        related_name='favorite'
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='users'
    )

    class Meta:
        verbose_name = _("Избранная книга")
        verbose_name_plural = _("Избранные книги")
        unique_together = ('user', 'book')

    def __str__(self) -> str:
        return f"{self.book} {self.user}"


class Rating(UUIDModel, TimestampMixin):
    book = models.ForeignKey(
        to='books.Book',
        on_delete=models.CASCADE,
        verbose_name=_('Книга'),
        related_name='ratings'
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
        related_name='ratings',
        blank=True,
        null=True
    )
    feedback = models.TextField(verbose_name=_('Текст отзыва'), null=True, blank=True)
    rated_on = models.DateTimeField(verbose_name=_("Дата рейтинга"), auto_now=True)
    value = models.SmallIntegerField(verbose_name=_("Значение рейтинга"), blank=False, null=False)

    class Meta:
        verbose_name = _("Оценка")
        verbose_name_plural = _("Оценки")
        unique_together = ('user', 'book')

    def clean(self):
        if self.value > 10:
            raise ValidationError("Максимально допустимая оценка книге - 10")

    def __str__(self) -> str:
        return f"{self.book} - {self.user}, {self.feedback}, {self.value}"
