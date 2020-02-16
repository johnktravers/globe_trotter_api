from django.db import models

class User(models.Model):
  email = models.EmailField(unique=True)
  name = models.CharField(max_length=100)
  api_key = models.CharField(max_length=32)

class Trip(models.Model):
  name = models.CharField(max_length=100)
  origin = models.CharField(max_length=100)
  origin_abbrev = models.CharField(max_length=3)
  origin_lat = models.CharField(max_length=100)
  origin_long = models.CharField(max_length=100)
  start_date = models.DateField()
  end_date = models.DateField()
  user = models.ForeignKey('User', on_delete=models.CASCADE)

class Destination(models.Model):
  location = models.CharField(max_length=100)
  abbrev = models.CharField(max_length=3)
  lat = models.CharField(max_length=100)
  long = models.CharField(max_length=100)

class TripDestination(models.Model):
  trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
  destination = models.ForeignKey('Destination', on_delete=models.CASCADE)

class Date(models.Model):
  date = models.DateField()
  trip_destination = models.ForeignKey('TripDestination', on_delete=models.CASCADE)
