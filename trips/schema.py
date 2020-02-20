import graphene
from graphene import ObjectType

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

class Query(ObjectType):
    all_trips = graphene.List(TripType, user_api_key=graphene.String(required=True))

    def resolve_all_trips(self, info, **kwargs):
        api_key = kwargs.get('user_api_key')
        user = User.objects.get(api_key = api_key)
        return Trip.objects.filter(user_id = user.id)
