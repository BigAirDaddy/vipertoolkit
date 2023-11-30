import requests
from config import numverify_api_key  # Import the API key from config.py

def numverify_check(api_key, phone_number, country_code, format=1):
  url = 'http://apilayer.net/api/validate'
  params = {
      'access_key': numverify_api_key,
      'number': phone_number,
      'country_code': country_code,
      'format': format
  }

  print("NumVerify API URL:", url)  # Print the constructed URL
  response = requests.get(url, params=params)

  try:
      data = response.json()
      print("Raw Response from NumVerify API:")
      print(data)

      if 'valid' in data:
          if data['valid']:
              print(f"Phone number information for {phone_number}:")
              print(f"Country: {data.get('country_name', 'N/A')}")
              print(f"Location: {data.get('location', 'N/A')}")
              print(f"Carrier: {data.get('carrier', 'N/A')}")
          else:
              print(f"The phone number {phone_number} is not valid.")
              print(f"Error: {data.get('error', {}).get('info', 'N/A')}")
      else:
          print("Unexpected response format from NumVerify API.")
  except ValueError:
      print("Error decoding JSON response.")

