import graphene

from graphene_django.types import DjangoObjectType
from trips.models import User, Trip, Destination, TripDestination, Date

class UserType(DjangoObjectType):
    class Meta:
        model = User

class TripType(DjangoObjectType):
    class Meta:
        model = Trip

class DestinationType(DjangoObjectType):
    class Meta:
        model = Destination

class TripDestinationType(DjangoObjectType):
    class Meta:
        model = TripDestination

class DateType(DjangoObjectType):
    class Meta:
        model = Date

class Query(object):
    all_trips = graphene.List(TripType)

    def resolve_all_trips(self, info, **kwargs):
        return Trip.objects.all()
