import json


from graphene_django.utils.testing import GraphQLTestCase
from globe_trotter.schema import schema
from trips.models import Trip, User, Destination, TripDestination, Activity

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

    def test_trip_creation(self):
        response = self.query(
            '''
            mutation {
                createTrip(userApiKey: "1234", origin: "Tokyo, Japan", name: "Tokyo Trip") {
                    trip {
                        name
                        origin
                        originAbbrev
                        originLat
                        originLong
                    }
                }
            }
            ''',
            op_name='createTrip'
        )

        expected = {
            "data": {
                "createTrip": {
                    "trip": {
                        "name": "Tokyo Trip",
                        "origin": "Tokyo, Japan",
                        "originAbbrev": "TYO",
                        "originLat": "35.6761919",
                        "originLong": "139.6503106"
                    }
                }
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)

    def test_create_trip_no_abbrev(self):
        response = self.query(
            '''
            mutation {
                createTrip(userApiKey: "1234", origin: "saint-jean-pied-de-port, france", name: "French trip") {
                    trip {
                        name
                        origin
                        originAbbrev
                        originLat
                        originLong
                    }
                }
            }
            ''',
            op_name='createTrip'
        )

        expected = {
            "data": {
                "createTrip": {
                    "trip": {
                        "name": "French trip",
                        "origin": "64220 Saint-Jean-Pied-de-Port, France",
                        "originAbbrev": "SAI",
                        "originLat": "43.163141",
                        "originLong": "-1.23811"
                    }
                }
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)

    def test_create_trip_invalid_location(self):
        response = self.query(
            '''
            mutation {
                createTrip(userApiKey: "1234", origin: "asdljkghafdadh", name: "Invalid Trip") {
                    trip {
                        name
                        origin
                        originAbbrev
                        originLat
                        originLong
                    }
                }
            }
            ''',
            op_name='createTrip'
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['errors'][0]['message'], 'Invalid location. Please try again.')

    def test_create_destination(self):
        response = self.query(
            '''
            mutation {
                createDestination(userApiKey: "1234", tripId: ''' + str(Trip.objects.first().id) + ''', location: "Stockholm, Sweden", startDate: "2020-03-23", endDate: "2020-03-30") {
                    destination {
                        location
                        abbrev
                        lat
                        long
                        tripdestinationSet {
                            startDate
                            endDate
                            trip {
                                name
                                origin
                                originAbbrev
                            }
                        }
                    }
                }
            }
            ''',
            op_name='createDestination'
        )

        expected = {
            "data": {
                "createDestination": {
                    "destination": {
                        "location": "Stockholm, Sweden",
                        "abbrev": "STO",
                        "lat": "59.32932349999999",
                        "long": "18.0685808",
                        "tripdestinationSet": [
                            {
                                "startDate": "2020-03-23",
                                "endDate": "2020-03-30",
                                "trip": {
                                    "name": "Spring Break",
                                    "origin": "Denver, CO, USA",
                                    "originAbbrev": "DEN",
                                }
                            }
                        ]
                    }
                }
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)

    def test_create_destination_invalid_location(self):
        response = self.query(
            '''
            mutation {
                createDestination(userApiKey: "1234", tripId: ''' + str(Trip.objects.first().id) + ''', location: "lfakjghhagdha", startDate: "2020-03-23", endDate: "2020-03-30") {
                    destination {
                        location
                        abbrev
                        lat
                        long
                        tripdestinationSet {
                            startDate
                            endDate
                            trip {
                                name
                                origin
                                originAbbrev
                            }
                        }
                    }
                }
            }
            ''',
            op_name='createDestination'
        )

        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['errors'][0]['message'], 'Invalid location. Please try again.')

    def test_create_activity(self):
        response = self.query(
            '''
            mutation {
                createActivity(userApiKey: "1234", tripDestinationId: ''' + str(TripDestination.objects.first().id) + ''', name: "Arc de Triomf", date: "2020-03-18", address: "Passeig de Sant Joan, s/n, 08010 Barcelona, Spain", category: "Landmarks & Historical Buildings", rating: 4.0, image: "https://s3-media3.fl.yelpcdn.com/bphoto/bmWXY-0so2VYI_lYv-pbVg/o.jpg", lat: 41.3910646236233, long: 2.1806213137548) {
                    activity {
                        name
                        date
                        address
                        category
                        rating
                        image
                        lat
                        long
                        tripDestination {
                            trip {
                                name
                            }
                            destination {
                                location
                                abbrev
                            }
                        }
                    }
                }
            }
            ''',
            op_name='createActivity'
        )

        expected = {
            "data": {
                "createActivity": {
                    "activity": {
                        "name": "Arc de Triomf",
                        "date": "2020-03-18",
                        "address": "Passeig de Sant Joan, s/n, 08010 Barcelona, Spain",
                        "category": "Landmarks & Historical Buildings",
                        "rating": 4,
                        "image": "https://s3-media3.fl.yelpcdn.com/bphoto/bmWXY-0so2VYI_lYv-pbVg/o.jpg",
                        "lat": "41.3910646236233",
                        "long": "2.1806213137548",
                        "tripDestination": {
                            "trip": {
                                "name": "Spring Break"
                            },
                            "destination": {
                                "location": "Barcelona, Spain",
                                "abbrev": "BCN"
                            }
                        }
                    }
                }
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)

    def test_delete_activity(self):
        activity = Activity.objects.create(
            name =  'Castell de Montjuïc',
            address =  'Carretera de Montjuïc, 66, 08038 Barcelona, Spain',
            date = '2022-03-18',
            category =  'Castles',
            rating =  4.0,
            image =  'https://s3-media1.fl.yelpcdn.com/bphoto/qvvaNwsAnLxa_g8_0IYiVA/o.jpg',
            lat =  '41.3633333212171',
            long =  '2.16618073941884',
            trip_destination = TripDestination.objects.first()
        )

        response = self.query(
            '''
            mutation {
                deleteActivity (userApiKey: "1234", activityId: ''' + str(activity.id) + ''') {
                    name
                    address
                    date
                    category
                    rating
                    image
                    lat
                    long

    def test_delete_trip(self):
        response = self.query(
            '''
            mutation {
                deleteTrip (userApiKey: "1234", tripId: ''' + str(Trip.objects.first().id) + ''') {
                    name
                    origin
                    originAbbrev
                    originLat
                    originLong
                }
            }
            ''',
            op_name='createActivity'
        )

        expected = {
            "data": {
                "deleteActivity": {
                    "name": "Castell de Montjuïc",
                    "address": "Carretera de Montjuïc, 66, 08038 Barcelona, Spain",
                    "date": "2022-03-18",
                    "category": "Castles",
                    "rating": 4.0,
                    "image": "https://s3-media1.fl.yelpcdn.com/bphoto/qvvaNwsAnLxa_g8_0IYiVA/o.jpg",
                    "lat": "41.3633333212171",
                    "long": "2.16618073941884"
                    
                "deleteTrip": {
                    "name": "Spring Break",
                    "origin": "Denver, CO, USA",
                    "originAbbrev": "DEN",
                    "originLat": "39.7392",
                    "originLong": "104.9903"
                }
            }
        }

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)
