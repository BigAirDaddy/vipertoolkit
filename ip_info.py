import requests
from colorama import Fore, Style
from config import access_key

def get_ip_info(ip):
    url = 'http://api.ipstack.com/' + ip + '?access_key=' + access_key
    response = requests.get(url)
    data = response.json()

    print((Fore.BLUE + Style.BRIGHT + 'Type: ' + Style.RESET_ALL) + data.get('type', 'N/A'))
    print((Fore.BLUE + Style.BRIGHT + 'Country: ' + Style.RESET_ALL) + data.get('country_name', 'N/A'))
    print((Fore.BLUE + Style.BRIGHT + 'Region: ' + Style.RESET_ALL) + data.get('region_name', 'N/A'))
    print((Fore.BLUE + Style.BRIGHT + 'City: ' + Style.RESET_ALL) + data.get('city', 'N/A'))
    print((Fore.BLUE + Style.BRIGHT + 'ZIP Code: ' + Style.RESET_ALL) + data.get('zip', 'N/A'))
    print((Fore.BLUE + Style.BRIGHT + 'Longitude: ' + Style.RESET_ALL) + str(data.get('longitude', 'N/A')))
    print((Fore.BLUE + Style.BRIGHT + 'Latitude: ' + Style.RESET_ALL) + str(data.get('latitude', 'N/A')))
