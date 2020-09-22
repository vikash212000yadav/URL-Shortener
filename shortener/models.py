from django.db import models

# Create your models here.
from hashlib import md5


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

        return super().save(*args, **kwargs)
