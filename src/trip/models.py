from django.conf import settings
from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title
