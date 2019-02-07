from django.db import models


class Trip(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    is_publid = models.BooleanField(default=True)

    def __str__(self):
        return self.title
