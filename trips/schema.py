import graphene
import requests
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

from graphene import ObjectType, Mutation

from graphene_django.types import DjangoObjectType
from trips.models import User, Trip, Destination, TripDestination, Activity

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
        params = {'address': origin, 'key': env("GEOCODE_API_KEY")}
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params).json()
        trip.origin = response['results'][0]['formatted_address']
        coordinates = response['results'][0]['geometry']['location']
        trip.origin_lat = coordinates['lat']
        trip.origin_long = coordinates['lng']
        params = {'term': trip.origin.split(",")[0], 'limit': 1}
        headers = {'APC-Auth-Secret': env("AIRPORT_CODES_API_SECRET"), 'APC-Auth': env("AIRPORT_CODES_API_KEY")}
        response = requests.get("https://www.air-port-codes.com/api/v1/multi", params=params, headers=headers).json()
        # import ipdb; ipdb.set_trace()
        trip.origin_abbrev = response['airports'][0]['iata']
        trip.save()

        return CreateTrip(trip=trip)
        # return CreateTrip(trip=1, name="Whatever", origin="Denver, CO", origin_lat="12.343", origin_long="123.34", origin_abbrev="DNV", user=user )



class Query(ObjectType):
    all_trips = graphene.List(TripType, user_api_key=graphene.String(required=True))

    def resolve_all_trips(self, info, **kwargs):
        api_key = kwargs.get('user_api_key')
        user = User.objects.get(api_key = api_key)
        return Trip.objects.filter(user_id = user.id)

class Mutation(ObjectType):
    create_trip = CreateTrip.Field()
