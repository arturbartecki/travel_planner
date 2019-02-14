from django.contrib import admin
from .models import Trip, TripDay
from ordered_model.admin import OrderedModelAdmin

admin.site.register(Trip)


class TripAdmin(OrderedModelAdmin):
    list_display = ('trip', 'content', 'order', 'move_up_down_links')


admin.site.register(TripDay, TripAdmin)
