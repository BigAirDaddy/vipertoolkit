import nmap
import threading
import sys
import time
from colorama import Fore, Style

spinner = [Fore.BLUE + Style.BRIGHT + "|", "/", "-", "\\" + Style.RESET_ALL]
spinner_speed = 0.1

stopped = False  # Define the 'stopped' variable

def perform_nmap_scan(ip, port, nmap_options):
    global stopped  # Use the global variable 'stopped'

    try:
        nm = nmap.PortScanner()
        scan_start_time = time.time()
        nm.scan(ip, port, arguments=nmap_options)
        stopped = True
        spinner_thread.join()
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

# Call the port scanning function
perform_nmap_scan(ip, port, nmap_options)
def update_spinner():
    while not stopped:
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(spinner_speed)
