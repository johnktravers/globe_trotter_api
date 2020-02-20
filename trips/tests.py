import json

from graphene_django.utils.testing import GraphQLTestCase
from globe_trotter.schema import schema
from trips.models import Trip, User, Destination, TripDestination

class TripsTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.maxDiff = None

        User.objects.create(
            email = 'john@gmail.com',
            name = 'John',
            api_key = '1234'
        )

        User.objects.create(
            email = 'zac@gmail.com',
            name = 'Zac',
            api_key = '4567'
        )

        Trip.objects.create(
            name = 'Spring Break',
            origin = 'Denver, CO, USA',
            origin_abbrev = 'DEN',
            origin_lat = '39.7392',
            origin_long = '104.9903',
            user = User.objects.first()
        )

        Destination.objects.create(
            location = "Barcelona, Spain",
            abbrev = "BCN",
            lat = "41.3851",
            long = "2.1734"
        )

        TripDestination.objects.create(
            start_date = "2020-03-16",
            end_date = "2020-03-19",
            trip = Trip.objects.first(),
            destination = Destination.objects.first()
        )

        Destination.objects.create(
            location = "Prague, Czech Republic",
            abbrev = "PRG",
            lat = "50.0755",
            long = "14.4378"
        )

        TripDestination.objects.create(
            start_date = "2020-03-19",
            end_date = "2020-03-23",
            trip = Trip.objects.last(),
            destination = Destination.objects.last()
        )


    def test_all_trips(self):
        response = self.query(
            '''
            query {
                allTrips(userApiKey: "1234") {
                    id
                    name
                    origin
                    originAbbrev
                    originLat
                    originLong
                    tripdestinationSet {
                        destination {
                            location
                            abbrev
                        }
                        startDate
                        endDate
                    }
                }
            }
            ''',
            op_name='Trip'
        )

        expected = {
          "data": {
            "allTrips": [
              {
                "id": "1",
                "name": "Spring Break",
                "origin": "Denver, CO, USA",
                "originAbbrev": "DEN",
                "originLat": "39.7392",
                "originLong": "104.9903",
                "tripdestinationSet": [
                  {
                    "destination": {
                      "location": "Barcelona, Spain",
                      "abbrev": "BCN"
                    },
                    "startDate": "2020-03-16",
                    "endDate": "2020-03-19"
                  },
                  {
                    "destination": {
                      "location": "Prague, Czech Republic",
                      "abbrev": "PRG"
                    },
                    "startDate": "2020-03-19",
                    "endDate": "2020-03-23"
                  }
                ]
              }
            ]
          }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)
