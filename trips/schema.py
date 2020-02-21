import graphene
import re

from graphene import ObjectType, Mutation
from graphene_django.types import DjangoObjectType
from trips.models import User, Trip, Destination, TripDestination, Activity
from trips.services import get_coordinates, get_airport_code

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

class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity

class CreateTrip(Mutation):
    trip = graphene.Field(TripType)

    class Arguments:
        user_api_key = graphene.String(required=True)
        name = graphene.String(required=True)
        origin = graphene.String(required=True)


    def mutate(self, info, user_api_key, name, origin):
        user = User.objects.get(api_key = user_api_key)
        trip = Trip(name=name, user=user)
        response = get_coordinates(origin)
        trip.origin = response[0]['formatted_address']
        trip.origin_lat = response[0]['geometry']['location']['lat']
        trip.origin_long = response[0]['geometry']['location']['lng']
        trip.origin_abbrev = get_airport_code(trip.origin)
        trip.save()

        return CreateTrip(trip=trip)


class Query(ObjectType):
    all_trips = graphene.List(TripType, user_api_key=graphene.String(required=True))

    def resolve_all_trips(self, info, **kwargs):
        api_key = kwargs.get('user_api_key')
        user = User.objects.get(api_key = api_key)
        return Trip.objects.filter(user_id = user.id)

class Mutation(ObjectType):
    create_trip = CreateTrip.Field()
