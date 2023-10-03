from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("UUID идентификатор"),
        editable=False,
        primary_key=True,
        default=uuid4,
    )

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        _("Время создания"), auto_now_add=True, db_index=True
    )
    changed_at = models.DateTimeField(
        _("Время последнего изменения"), auto_now=True, db_index=True
    )

    class Meta:
        abstract = True
