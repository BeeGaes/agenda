from datetime import datetime
from django.db import models
from django.urls import reverse

from calendarapp.models import EventAbstract
from accounts.models import User

class UnitManager(models.Manager):
    """ Unit manager """

    def get_all_units(self, user):
        units = Unit.objects.filter(user=user, is_active=True, is_deleted=False)
        return units

    def get_operating_units(self, user):
        operating_units = Unit.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("id")
        return operating_units

class Unit(EventAbstract):
    """ Unit model """
    division = models.CharField(max_length=200)
    PIC = models.CharField(max_length=200)

    objects = UnitManager()

    def __str__(self):
        return self.division

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.division} </a>'

class PlaceManager(models.Manager):
    """ Place manager """

    def get_all_places(self, user):
        places = Place.objects.filter(user=user, is_active=True, is_deleted=False)
        return places

    def get_occupied_places(self, user):
        occupied_places = Place.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("id")
        return occupied_places
class Place(EventAbstract):
    """ Place model """
    room = models.CharField(max_length=200)
    capacity = models.IntegerField()

    objects = PlaceManager()

    def __str__(self):
        return self.room

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.room} </a>'

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    division = models.ForeignKey(Unit, on_delete=models.CASCADE)
    room = models.ForeignKey(Place, on_delete=models.CASCADE)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    

