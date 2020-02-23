# GlobeTrotter API

## Description

GlobeTrotter is an application used to plan multi-leg adventures and create day-by-day itineraries for each stop along the way. This API serves as the backend for the application. It utilizes GraphQL to handle database queries and mutations, as well as one RESTful endpoint to retrieve and format data from the Yelp API.

This API is deployed to Heroku [here](https://globe-trotter-api.herokuapp.com/graphql/), and the frontend application can be found [here](https://github.com/sertmer/GlobeTrotter).

## Initial Setup

If Python 3 and/or Pipenv are not installed on your machine, please execute the following commands before continuing:

```
brew install python3
brew install pipenv
```

In order to setup the repo and install dependencies, navigate into your desired directory and execute the following:

```
git clone git@github.com:johnktravers/globe_trotter_api.git
cd globe_trotter_api
pipenv shell
pipenv install
```

Now create, migrate, and seed the development database by executing these commands:

```
psql
CREATE DATABASE globe_trotter_api_dev
\q
python3 manage.py migrate
python3 manage.py loaddata trips.json
```

### Environment Variables

The following environment variables are required. These can be added to a `.env` file, for which integration is already established. All API keys are free to obtain.

- **DATABASE_URL** set to `postgres://postgres@localhost:5432/globe_trotter_api_dev`
- **GEOCODE_API_KEY** set to your registered [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/start) key
- **AIRPORT_CODES_API_KEY** set to your registered [Airport Codes API](https://www.air-port-codes.com/airport-codes-api/overview/) key
- **AIRPORT_CODES_API_SECRET** set to the secret given to you by the [Airport Codes API](https://www.air-port-codes.com/airport-codes-api/overview/)
- **YELP_API_KEY** set to your registered [Yelp Fusion API](https://www.yelp.com/fusion) key


## Testing

In order to make sure setup was executed properly, run the test suite by executing the following command:

```
python3 manage.py test
```

If you would like to examine test coverage, execute the following instead:

```
coverage run --source='.' manage.py test
open htmlcov/index.html
```

## How to Use / Endpoints

### GraphQL Endpoint

The GraphQL endpoint is found by making `POST` requests to `/graphql/`, regardless of whether a query or mutation is desired. This endpoint interacts with the database to create, read, update, or delete information that a user has saved, such as trips, destinations, and activities. The following are the available attributes for each resource:

| User    | Trip                 | Destination          | TripDestination | Activity          |
|---------|----------------------|----------------------|-----------------|-------------------|
| `id`    | `id`                 | `id`                 | `id`            | `id`              |
| `name`  | `name`               | `location`           | `trip`          | `name`            |
| `email` | `origin`             | `abbrev`             | `destination`   | `address`         |
|         | `originAbbrev`       | `lat`                | `startDate`     | `category`        |
|         | `originLat`          | `long`               | `endDate`       | `rating`          |
|         | `originLong`         | `tripdestinationSet` | `activitySet`   | `image`           |
|         | `tripdestinationSet` | `tripSet`            |                 | `lat`             |
|         | `destinationSet`     |                      |                 | `long`            |
|         | `user`               |                      |                 | `date`            |
|         |                      |                      |                 | `tripDestination` |

Each request requires authentication through a `userApiKey` parameter, which is created with a user's account and is passed between the frontend and backend applications.

#### allTrips Query

This query retrieves an array of all of a user's trips. See the table above for attributes that can be added to the query.

Request body example:
```
query {
  allTrips(userApiKey: "<USER_API_KEY>") {
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
        lat
        long }
      startDate
      endDate
    }
  }
}
```

Response body example:
```
{
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
              "abbrev": "BCN",
              "lat": "41.3851",
              "long": "2.1734"
            },
            "startDate": "2020-03-16",
            "endDate": "2020-03-19"
          },
          {
            "destination": {
              "location": "Prague, Czech Republic",
              "abbrev": "PRG",
              "lat": "50.0755",
              "long": "14.4378"
            },
            "startDate": "2020-03-19",
            "endDate": "2020-03-23"
          }
        ]
      }
    ]
  }
}
```

#### createTrip Mutation

This mutation creates a trip for an authenticated user. The required input parameters are `name` and `origin`. See the table above for attributes that can be added to the mutation.

Request body example:
```
mutation {
  createTrip(userApiKey: "<USER_API_KEY>", name: "Northern Lights", origin: "Reykjavik, Iceland") {
    trip {
      id
      name
      origin
      originAbbrev
      originLat
      originLong
    }
  }
}
```

Response body example:
```
{
  "data": {
    "createTrip": {
      "trip": {
        "id": "2",
        "name": "Northern Lights",
        "origin": "Reykjavík, Iceland",
        "originAbbrev": "REK",
        "originLat": "64.146582",
        "originLong": "-21.9426354"
      }
    }
  }
}
```

#### createDestination Mutation

This mutation creates a destination for an authenticated user's trip given the `tripId`, `location`, `startDate`, and `endDate`. See the table above for attributes that can be added to the mutation.

Request body example:
```
mutation {
  createDestination(userApiKey: "b9aead4b955bccb5c57ef830580f3de5", tripId: 2, location: "Stockholm, Sweden", startDate: "2021-12-18", endDate: "2021-12-24") {
    destination {
      id
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
        }
      }
    }
  }
}
```

Response body example:
```
{
  "data": {
    "createDestination": {
      "destination": {
        "id": "3",
        "location": "Stockholm, Sweden",
        "abbrev": "STO",
        "lat": "59.32932349999999",
        "long": "18.0685808",
        "tripdestinationSet": [
          {
            "startDate": "2021-12-18",
            "endDate": "2021-12-24",
            "trip": {
              "name": "Northern Lights",
              "origin": "Reykjavík, Iceland"
            }
          }
        ]
      }
    }
  }
}
```

#### deleteActivity Mutation

This mutation deletes an activity by `activityId` for an authenticated user. All activity attributes except relationships to other tables can be added to the mutation response.

Request body example:
```
mutation {
  deleteActivity (userApiKey: "<USER_API_KEY>", activityId: 2) {
    id
    name
    address
    date
    category
    rating
    image
    lat
    long
  }
}
```

Response body example:
```
{
  "data": {
    "deleteActivity": {
      "id": "2",
      "name": "Castell de Montjuïc",
      "address": "Carretera de Montjuïc, 66, 08038 Barcelona, Spain",
      "date": "2022-03-18",
      "category": "Castles",
      "rating": 4.0,
      "image": "https://s3-media1.fl.yelpcdn.com/bphoto/qvvaNwsAnLxa_g8_0IYiVA/o.jpg",
      "lat": "41.3633333212171",
      "long": "2.16618073941884"
    }
  }
}
```

### Yelp Activities RESTful Endpoint

This endpoint is used to retrieve and format the top 20 landmarks for a given latitude and longitude. The endpoint can be accessed by sending a `GET` request to `/api/v1/yelp_activities/?lat=<LATITUDE>&long=<Longitude>`. No user authentication is necessary.

Response body example:
```
{
  "activities": [
    {
      "name": "Pantheon - Basilica di Santa Maria ad Martyres",
      "address": "Piazza della Rotonda, 00186 Rome, Italy",
      "category": "Churches",
      "rating": 4.5,
      "image": "https://s3-media3.fl.yelpcdn.com/bphoto/wDcbtQyxePfBYfHHXYiwGw/o.jpg",
      "lat": 41.898614,
      "long": 12.476869
    },
    {
      "name": "Colosseo",
      "address": "Piazza del Colosseo 1, 00184 Rome, Italy",
      "category": "Local Flavor",
      "rating": 4.5,
      "image": "https://s3-media1.fl.yelpcdn.com/bphoto/QcMxqdZmJTMpeeuT_NfHAg/o.jpg",
      "lat": 41.8902496828181,
      "long": 12.4922484062616
    },
    .
    .
    .
  ]
}
```

## Focus Areas

- Using GraphQL to create a CRUD API
- Gaining familiarity with Python and Django applications

## Technologies and Frameworks Used

- Python
- Django
- GraphQL
- PostgresQL
- UnitTest
- Travis CI

## APIs Consumed

- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/start)
- [Airport Codes API](https://www.air-port-codes.com/airport-codes-api/overview/)
- [Yelp Fusion API](https://www.yelp.com/fusion)

## Database Schema

![schema diagram](https://user-images.githubusercontent.com/46035439/75104591-861ba400-55c8-11ea-9736-bde6ed2bb283.png)

## Core Contributors

- [Zac Isaacson](https://github.com/zacisaacson)
- [John Travers](https://github.com/johnktravers)
