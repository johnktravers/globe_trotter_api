import requests
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

def get_coordinates(location):
    params = {'address': location, 'key': env("GEOCODE_API_KEY")}
    return requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params).json()['results']

def get_airport_code(location):
    params = {'term': location.split(",")[0], 'limit': 1}
    headers = {'APC-Auth-Secret': env("AIRPORT_CODES_API_SECRET"), 'APC-Auth': env("AIRPORT_CODES_API_KEY")}
    response = requests.get("https://www.air-port-codes.com/api/v1/multi", params=params, headers=headers).json()
    if 'airports' in response:
        return response['airports'][0]['iata']
    else:
        return re.findall("[a-zA-Z]+", location)[0][:3].upper()
