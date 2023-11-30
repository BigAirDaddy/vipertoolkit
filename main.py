from colorama import Fore, Style
from port_scan import perform_nmap_scan
from ip_info import get_ip_info
from shodan_search import shodan_search
from phone_number import numverify_check
from config import numverify_api_key

# ... (Other imports and global variables)

if __name__ == "__main__":
    while True:
        print(Fore.RED + Style.BRIGHT + "Welcome to the VIPER Toolkit!\n" + Style.RESET_ALL)
        print(Fore.GREEN + Style.BRIGHT + "Select Your Tool\n")
        print(Fore.BLUE + Style.BRIGHT + "1. Port Scanner (1)\n")
        print(Fore.BLUE + Style.BRIGHT + "2. IP Information (2)\n")
        print(Fore.BLUE + Style.BRIGHT + "3. Shodan Search (3)\n")
        print(Fore.BLUE + Style.BRIGHT + "4. Phone Number Search (4)\n")

        a = input(Fore.BLUE + Style.BRIGHT + "Enter Your Choice (or 'q' to quit):\n" + Style.RESET_ALL)

        if a == 'q':
            break  # Exit the program if the user enters 'q'

        if a in ("1", "2", "3"):
            ip = input(Fore.RED + Style.BRIGHT + 'Enter the IP address or phone number you would like to use: \n' + Style.RESET_ALL)

      
        if a == "4":
          phone_number = input(Fore.RED + Style.BRIGHT + 'Enter the phone number you would like to search without the country code:\n' + Style.RESET_ALL)
          country_code = input(Fore.RED + Style.BRIGHT + 'Enter the country you would like to use ex(US):\n' + Style.RESET_ALL)
          numverify_check(numverify_api_key, phone_number, country_code)
          format = 1

        if a == '2':
            get_ip_info(ip)

        if a == '3':
            shodan_search(ip)


        if a == '1':
              # Port scanning inputs
              scan_type = input(Fore.RED + Style.BRIGHT + 'Choose the Nmap scan type (quick, regular, or Aggressive): ' + Style.RESET_ALL)
              if scan_type == 'quick':
                  nmap_options = '-F'  # Fast scan with common ports
              elif scan_type == 'regular':
                  nmap_options = ''  # Default Nmap options (regular scan)
              elif scan_type == 'Aggressive':
                  nmap_options = '-T4'  # Aggressive fast scan
              else:
                  print("Invalid scan type. Using a regular scan.")
                  nmap_options = ''  # Default Nmap options (regular scan)

              answer = input('Would you like to scan a specific range of ports on this address? (y/n) ')
              if answer.lower() == 'y':
                  port = input('Enter the ports you would like to scan (or press Enter to scan all)\n')
                  if not port:
                      port = '0-65535'
                  else:
                      try:
                          int(port)
                      except ValueError:
                          print("Invalid input for port. Using default range.")
                          port = '0-65535'
              else:
                  port = '0-65535'  # Default to scanning all ports

              vuln_scan = input('Do you want to run vulnerability detection scripts? (y/n) ')
              if vuln_scan.lower() == 'y':
                  nmap_options += ' --script vuln'
                  print(Fore.GREEN + Style.BRIGHT + 'Scanning for open ports and vulnerabilities\n' + Style.RESET_ALL)

              # Call the port scanning function
              perform_nmap_scan(ip, port, nmap_options) here
            pass

        print(Fore.RED + Style.BRIGHT + "Thank you for using the VIPER Toolkit!\n" + Style.RESET_ALL)
