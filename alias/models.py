from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from .validators import check_overlaps


class Alias(models.Model):
    alias = models.CharField(max_length=90)

    target = models.CharField(max_length=24)

    start = models.DateTimeField(default=timezone.now())

    end = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.alias

    def save(self, update=False, *args, **kwargs):
        if update or check_overlaps(Alias, self):
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Alias lifetime should not overlap same name alias on the target.', code='invalid')
