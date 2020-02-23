import unittest
import json
from django.test import Client

class YelpActivitiesTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/api/v1/yelp_activities/?lat=41.9027835&long=12.4963655')
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['activities']), 20)

        self.assertTrue(data['activities'][0]['name'])
        self.assertTrue(data['activities'][0]['address'])
        self.assertTrue(data['activities'][0]['category'])
        self.assertTrue(type(data['activities'][0]['rating']) is float)
        self.assertTrue(type(data['activities'][0]['lat']) is float)
        self.assertTrue(type(data['activities'][0]['long']) is float)
