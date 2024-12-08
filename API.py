import requests
from tkinter import messagebox
def fetch_weather_data(city):
    # define the API 
    api_key = "f6c45028119c4cd4994152515242811"
    base_url = "http://api.weatherapi.com/v1/current.json?key=f6c45028119c4cd4994152515242811&q="
    base_url+=city
    # build request URL
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  
        "lang": "zh_cn"  
    }

# send request
    response = requests.get(base_url, params=params)

    # check the data availability
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed: {response.status_code}")
        print(f"Error: {response.text}")

def get_location():
    """Get the user's current location based on IP address"""
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            country = data.get("country")
            return city, country
        else:
            raise Exception("Failed to fetch location.")
    except Exception as e:
        messagebox.showerror("Location Error", f"Could not determine location: {e}")
        return None, None
    

# Google Maps API Key

def get_user_location():
    """Fetch user's approximate location using IP Geolocation."""
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            lat = data.get("lat")
            lon = data.get("lon")
            return lat, lon
        else:
            raise Exception("Failed to fetch location.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def find_restaurants(lat, lon, radius=2000):
    """Find nearby restaurants using Google Places API."""
    API_KEY = "AIzaSyDfWnpjktG1qojKJLA7TUUdqqWCUu5A1fY"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{lat},{lon}",
        "radius": radius,  # Search radius in meters
        "type": "restaurant"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            restaurants = []
            for place in results:
                name = place.get("name")
                address = place.get("vicinity")
                rating = place.get("rating", "N/A")
                restaurants.append((name, address, rating))
            return restaurants
        else:
            raise Exception("Failed to fetch restaurant data.")
    except Exception as e:
        print(f"Error: {e}")
        return []

# Main Script
if __name__ == "__main__":
    # Step 1: Get user location
    lat, lon = get_user_location()
    if lat is None or lon is None:
        print("Could not determine your location.")
    else:
        print(f"Your location: Latitude={lat}, Longitude={lon}")

        # Step 2: Find restaurants
        restaurants = find_restaurants(lat, lon)
        if not restaurants:
            print("No restaurants found nearby.")
        else:
            print("Nearby Restaurants:")
            for i, (name, address, rating) in enumerate(restaurants, start=1):
                print(f"{i}. {name} - {address} (Rating: {rating})")
