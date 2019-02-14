from django.conf import settings
from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from ordered_model.models import OrderedModel


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


class TripDay(OrderedModel):
    """Ordered model """
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    content = models.TextField()
    order_with_respect_to = 'trip'

    class Meta(OrderedModel.Meta):
        ordering = ('trip', 'order')

    def __str__(self):
        return f'Day {self.order + 1} in trip {self.trip}'


@receiver(post_delete, sender=TripDay)
def reshuffle(sender, instance, using, *args, **kwargs):
    """Function reshuffles ordering after delete()"""
    query = TripDay.objects.filter(trip=instance.trip)
    for count, obj in enumerate(query, 0):
        print(count)
        obj.to(count)
        count += 1
