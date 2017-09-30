from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from ..LogReg.models import User

class TripManager(models.Manager):
    def addtrip(self, user, destination, description, date_start, date_end, csrfmiddlewaretoken):
        messagelist = []
        
        destination = destination[0]
        if not destination:
            messagelist.append("Must include Destination")
        
        if not description:
            messagelist.append("Must include Description")
        description = description[0]
        
        date_start = datetime.strptime(date_start[0], '%Y-%m-%d')
        if date_start < datetime.today():
            messagelist.append("Travel Dates must be future-dated")
        
        date_end = datetime.strptime(date_end[0], '%Y-%m-%d')
        if date_end < date_start:
            messagelist.append("'Travel Date To' cannot be before 'Travel Date From'")
        
        if len(messagelist) == 0:
            new_trip = Trip.objects.create(user=user, destination=destination, description=description, date_start=date_start, date_end=date_end)
            return (True, new_trip.id)
        else:
            return (False, messagelist)
    def jointrip(self, user_id, trip_id):
        user = User.objects.get(id=user_id)
        trip = Trip.objects.get(id=trip_id)
        
        if trip.user == user:
            return (False, "Already attending trip")
        elif Guest.objects.filter(trip=trip).filter(user=user):
            return (False, "Already attending trip")
        Guest.objects.create(user=user, trip=trip)
        return (True, "Successfully joined trip!")

class Trip(models.Model):
    user = models.ForeignKey(User, related_name="tripuser")
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=120)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripManager = TripManager()
    objects = models.Manager()

class Guest(models.Model):
    user = models.ForeignKey(User, related_name="guestuser")
    trip = models.ForeignKey(Trip, related_name="guesttrip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)