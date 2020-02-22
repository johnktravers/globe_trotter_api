import graphene

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

class CreateDestination(Mutation):
    destination = graphene.Field(DestinationType)

    class Arguments:
        user_api_key = graphene.String(required=True)
        trip_id = graphene.ID(required=True)
        location = graphene.String(required= True)
        start_date = graphene.types.datetime.Date(required=True)
        end_date = graphene.types.datetime.Date(required=True)

    def mutate(self, info, user_api_key, trip_id, location, start_date, end_date):
        user = User.objects.get(api_key = user_api_key)
        trip = Trip.objects.filter(user_id=user.id).get(id=trip_id)
        destination = Destination()
        response = get_coordinates(location)
        destination.location = response[0]['formatted_address']
        destination.lat = response[0]['geometry']['location']['lat']
        destination.long = response[0]['geometry']['location']['lng']
        destination.abbrev = get_airport_code(destination.location)
        destination.save()

        trip_destination = TripDestination(start_date=start_date, end_date=end_date, trip=trip, destination=destination)
        trip_destination.save()

        return CreateDestination(destination=destination)



class Query(ObjectType):
    all_trips = graphene.List(TripType, user_api_key=graphene.String(required=True))

    def resolve_all_trips(self, info, **kwargs):
        api_key = kwargs.get('user_api_key')
        user = User.objects.get(api_key = api_key)
        return Trip.objects.filter(user_id = user.id)

class Mutation(ObjectType):
    create_trip = CreateTrip.Field()
    create_destination = CreateDestination.Field()
