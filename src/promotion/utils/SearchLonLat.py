import requests

def search_lon_lat(address):
    url = f'https://nominatim.openstreetmap.org/search?format=json&q={address}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        if data:
            print(f"search_lon_lat result: {data}")
            
            if 'address' in data and 'street' in data['address']:
                lat = data[0]['lat']
                lon = data[0]['lon']
                ge = {'address': data['address']['street'], 'latitude': lat, 'longitude': lon}
                print("clean data", ge)
                return ge
    return None
