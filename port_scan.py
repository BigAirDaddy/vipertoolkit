import nmap
import threading
import sys
import time
from colorama import Fore, Style

spinner = [Fore.BLUE + Style.BRIGHT + "|", "/", "-", "\\" + Style.RESET_ALL]
spinner_speed = 0.1

stopped = False  # Define the 'stopped' variable
update_spinner_thread = None  # Declare the update_spinner_thread variable

def perform_nmap_scan():
    global stopped, update_spinner_thread  # Use the global variables 'stopped' and 'update_spinner_thread'

    ip = input(Fore.RED + Style.BRIGHT + 'Enter the IP address you would like to scan: \n' + Style.RESET_ALL)

    print(Fore.RED + Style.BRIGHT + 'Choose the Nmap scan type:\n ' + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + '1. TCP SYN Scan (sS)\n')
    print('2. TCP Connect Scan (sT)\n')
    print('3. UDP Scan (sU)\n')
    print('4. ACK Scan (sA)\n')
    print('5. Window Scan (sW)\n')
    print('6. Idle Scan (sI)\n')
    print('7. XMAS Tree Scan (sX)\n')
    print('8. NULL Scan (sN)\n')
    print('9. Basic TCP Scan (sY)\n')

    scan_type = input('Enter your choice number: ' + Style.RESET_ALL)

    if scan_type == '1':
        nmap_options = '-sS'  # TCP SYN Scan
    elif scan_type == '2':
        nmap_options = '-sT'  # TCP Connect Scan
    elif scan_type == '3':
        nmap_options = '-sU'  # UDP Scan
    elif scan_type == '4':
        nmap_options = '-sA'  # ACK Scan
    elif scan_type == '5':
        nmap_options = '-sW'  # Window Scan
    elif scan_type == '6':
        nmap_options = '-sI zombie'  # Idle Scan (requires a zombie system)
    elif scan_type == '7':
        nmap_options = '-sX'  # XMAS Tree Scan
    elif scan_type == '8':
        nmap_options = '-sN'  # NULL Scan
    elif scan_type == '9':
        nmap_options = '-sY'
    else:
        print("Invalid scan type. Using a regular scan.")
        nmap_options = ''  # Default Nmap options (regular scan)

    answer = input(Fore.RED + Style.BRIGHT + 'Would you like to scan a specific range of ports on this address? (y/n) ' + Style.RESET_ALL)
    if answer.lower() == 'y':
        port = input(Fore.RED + Style.BRIGHT + 'Enter the ports you would like to scan:\n' + Style.RESET_ALL)
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

    vuln_scan = input(Fore.RED + Style.BRIGHT + 'Do you want to run vulnerability detection scripts? (y/n) ' + Style.RESET_ALL)
    if vuln_scan.lower() == 'y':
        nmap_options += ' --script vuln'
        print(Fore.GREEN + Style.BRIGHT + 'Scanning for open ports and vulnerabilities\n' + Style.RESET_ALL)

    try:
        nm = nmap.PortScanner()
        scan_start_time = time.time()

        # Start the spinner thread
        update_spinner_thread = threading.Thread(target=update_spinner)
        update_spinner_thread.start()

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

if __name__ == "__main__":
    perform_nmap_scan()
