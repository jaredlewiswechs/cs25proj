import requests
import json
import time
import webbrowser # To optionally open the location on a map

# API endpoint for current ISS location
API_URL = "http://api.open-notify.org/iss-now.json"
MAP_URL_TEMPLATE = "https://www.google.com/maps/search/?api=1&query={lat},{lon}"

def get_iss_location():
    """Fetches the current latitude and longitude of the ISS."""
    try:
        response = requests.get(API_URL, timeout=5) # Add a timeout
        # Raise an exception if the request was unsuccessful (e.g., 404, 500)
        response.raise_for_status()
        data = response.json()

        if data.get("message") == "success":
            latitude = data["iss_position"]["latitude"]
            longitude = data["iss_position"]["longitude"]
            timestamp = data["timestamp"]
            return float(latitude), float(longitude), timestamp
        else:
            print("API response message was not 'success'.")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS data: {e}")
        return None, None, None
    except json.JSONDecodeError:
        print("Error decoding JSON response from API.")
        return None, None, None
    except KeyError:
        print("Unexpected format in API response.")
        return None, None, None

# --- Main Execution ---
if __name__ == "__main__":
    print("Fetching real-time ISS location...")
    print("Press Ctrl+C to stop.")

    first_run = True
    try:
        while True:
            lat, lon, ts = get_iss_location()

            if lat is not None and lon is not None:
                print(f"\nTimestamp: {time.ctime(ts)}")
                print(f"Current ISS Location:")
                print(f"  Latitude:  {lat:.4f}")
                print(f"  Longitude: {lon:.4f}")

                # Optionally open the map on the first successful fetch
                if first_run:
                   map_url = MAP_URL_TEMPLATE.format(lat=lat, lon=lon)
                   print(f"View on map: {map_url}")
                   try:
                       # Try to open in web browser (might not work on all systems/environments)
                       webbrowser.open(map_url)
                   except Exception as e:
                       print(f"(Could not automatically open browser: {e})")
                   first_run = False # Don't open it repeatedly

            else:
                print("Could not retrieve location.")

            # Wait for a bit before checking again
            time.sleep(10) # Check every 10 seconds

    except KeyboardInterrupt:
        print("\nStopping ISS tracker.")