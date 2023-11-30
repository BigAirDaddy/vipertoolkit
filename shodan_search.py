import shodan
from colorama import Fore, Style
from config import shodan_api_key

def shodan_search(ip):
    try:
        api = shodan.Shodan(shodan_api_key)
        result = api.host(ip)

        print(Fore.BLUE + Style.BRIGHT + 'Shodan Information for ' + ip + ':' + Style.RESET_ALL)
        print(Fore.BLUE + Style.BRIGHT + f"IP: {result['ip_str']}")
        print(f"Organization: {result.get('org', 'N/A')}")
        print(f"Operating System: {result.get('os', 'N/A')}")
        print(f"Ports: {result.get('ports', 'N/A')}")
        print(f"Hostnames: {', '.join(result.get('hostnames', ['N/A']))}")

        vulnerabilities = result.get('vulns', {})
        if isinstance(vulnerabilities, list):
            print(Fore.BLUE + Style.BRIGHT + "Vulnerabilities: No vulnerabilities found" + Style.RESET_ALL)
        else:
            print(f"Vulnerabilities: {', '.join(vulnerabilities.keys())}" + Style.RESET_ALL)

        print(Fore.BLUE + Style.BRIGHT + "Open Ports and Banners:" + Style.RESET_ALL)
        for item in result['data']:
            print(f"Port: {item['port']}")
            print(f"Banner: {item['data']}")
            print("-" * 30)

    except shodan.exception.APIError as e:
        print(f"Shodan Error: {e}")
