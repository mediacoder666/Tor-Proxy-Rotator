# Tor Proxy Rotator

## Description

Tor Proxy Rotator is a Python tool that automatically starts and manages a Tor proxy with IP address rotation at specified intervals.

## Features

- Automatic Tor process startup
- IP address rotation at defined time intervals
- SOCKS5 proxy support
- Automatic detection and handling of occupied ports
- Automatic Tor executable path discovery
- Current IP address verification through Tor proxy
- Easy termination via Ctrl+C

## Requirements

- Python 3.x
- Libraries: `stem`, `requests`, `psutil`
- Tor executable file (`tor.exe`)

### Installing Python Dependencies

pip install stem requests psutil

### Configuration

To change the ports used by the program and the time between IP changes, edit the `tpr.py` file.
At the end of the script you will find...
SOCKS_PORT = 9052      # Recommended port (safe and rarely used)
CONTROL_PORT = 9051    # Control port
ROTATION_INTERVAL = 10 # Time between IP changes, specified in seconds

### Created Proxy Address

- localhost:9052
- 127.0.0.1:9052

### Adding Proxy to Browsers

#Chrome#

"Settings"
"System"
"Open your computer's proxy settings"
"Manual proxy configuration"
Enter the address and port number
Click OK to save changes.

#Firefox#

"Options"
"Network"
"Manual proxy configuration"
Enter the address and port number
Click OK to save changes.
Proxy address: localhost:9052

### Nmap Support

Nmap does not natively support SOCKS proxies.
To scan through Tor, use the torsocks tool.
torsocks nmap -sT -Pn example.com

### Adding Proxy to Python Script

tor4python.py

### Author

mediacoder666