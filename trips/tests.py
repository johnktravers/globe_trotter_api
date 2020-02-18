import json

from graphene_django.utils.testing import GraphQLTestCase
from globe_trotter.schema import schema
from trips.models import Trip, User

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
            start_date = '2020-03-16',
            end_date = '2020-03-23',
            user = User.objects.first()
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
                    startDate
                    endDate
                    user {
                        id
                        name
                        email
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
                        "startDate": "2020-03-16",
                        "endDate": "2020-03-23",
                        "user": {
                            "id": "1",
                            "name": "John",
                            "email": "john@gmail.com"
                        }
                    }
                ]
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)
