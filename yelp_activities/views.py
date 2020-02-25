from django.shortcuts import render
from django.http import JsonResponse
import requests
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

def yelp_activities(request):
    lat = request.GET.get('lat')
    long = request.GET.get('long')
    if lat and long:
        headers = {'Authorization': f'Bearer {env("YELP_API_KEY")}'}
        params = {'latitude': lat, 'longitude': long, 'categories': 'landmarks', 'sort_by': 'rating'}
        businesses = requests.get('https://api.yelp.com/v3/businesses/search', params=params, headers=headers).json()['businesses']

        formatted_data = {'activities': []}
        for business in businesses:
            formatted_data['activities'].append({
                'name': business['name'],
                'address': ', '.join(business['location']['display_address']),
                'category': business['categories'][0]['title'],
                'rating': business['rating'],
                'image': business['image_url'],
                'lat': business['coordinates']['latitude'],
                'long': business['coordinates']['longitude']
            })
        return JsonResponse(formatted_data)
    else:
        errors = {'errors': [{"message": "Please specify a location by including lat and long params in the URL."}]}
        return JsonResponse(errors, status=400)
