import nmap
import threading
import sys
import time
from colorama import Fore, Style

spinner = [Fore.BLUE + Style.BRIGHT + "|", "/", "-", "\\" + Style.RESET_ALL]
spinner_speed = 0.1

stopped = False  # Define the 'stopped' variable

def perform_nmap_scan():
    global stopped  # Use the global variable 'stopped'

    ip = input(Fore.RED + Style.BRIGHT + 'Enter the IP address you would like to scan: \n' + Style.RESET_ALL)
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

    try:
        nm = nmap.PortScanner()
        scan_start_time = time.time()
        nm.scan(ip, port, arguments=nmap_options)
        stopped = True
        update_spinner_thread.join()
        print(Fore.RED + Style.BRIGHT + "Scan results:" + Style.RESET_ALL)

        for host in nm.all_hosts():
            print(f"Host: {host}")
            scan_result = nm[host]
            for protocol in scan_result.all_protocols():
                print(f"Protocol: {protocol}")
                port_info = scan_result[protocol]
                for port in port_info:
                    state = port_info[port]['state']
                    service = port_info[port]['name']
                    product = port_info[port].get('product', 'N/A')
                    version = port_info[port].get('version', 'N/A')
                    extrainfo = port_info[port].get('extrainfo', 'N/A')

                    print(f"Port: {port} - State: {state}")
                    print(f"  Service: {service}")
                    print(f"  Product: {product}")
                    print(f"  Version: {version}")
                    print(f"  Extra Info: {extrainfo}")

        elapsed_scan_time = time.time() - scan_start_time
        print(f"Scan Completed in {elapsed_scan_time:.2f} seconds")

    except nmap.nmap.PortScannerError as e:
        print(f"Error occurred while scanning: {str(e)}")
        print("Scan failed. Please check your input or Nmap configuration")

def update_spinner():
    while not stopped:
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(spinner_speed)

