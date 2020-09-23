from django.db import models

# Create your models here.
from hashlib import md5
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from graphql import GraphQLError


# Do not use md5 in production due to collision issues :)

class URL(models.Model):
    url_o = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.url_o.encode()).hexdigest()[:10]

        validate = URLValidator()
        try:
            validate(self.url_o)
        except ValidationError as e:
            raise GraphQLError('INVALID URL!')

        return super().save(*args, **kwargs)
