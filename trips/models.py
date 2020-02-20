from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=32)

class Destination(models.Model):
    location = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=3)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)

class Trip(models.Model):
    name = models.CharField(max_length=100, unique=True)
    origin = models.CharField(max_length=100)
    origin_abbrev = models.CharField(max_length=3)
    origin_lat = models.CharField(max_length=100)
    origin_long = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    destinations = models.ManyToManyField(Destination, through='TripDestination')

class TripDestination(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)

class Activity(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.DateField()
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    image = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    long = models.CharField(max_length=100)
    trip_destination = models.ForeignKey('TripDestination', on_delete=models.CASCADE)
