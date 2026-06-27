import time
import subprocess
import requests
from stem import Signal
from stem.control import Controller
import threading
import os
import sys
import psutil
import socket

class TorProxyRotator:
    def __init__(self, socks_port=9052, control_port=9051, rotation_interval=300, tor_path=None):
        self.socks_port = socks_port
        self.control_port = control_port
        self.rotation_interval = rotation_interval
        self.is_running = False
        self.tor_process = None
        self.tor_path = tor_path
        
    def check_port_available(self, port):
        """Checks if the port is available"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result != 0  # 0 means the port is occupied
        except:
            return True
    
    def find_available_port(self, start_port=9052, max_attempts=10):
        """Finds an available port starting from start_port"""
        for port in range(start_port, start_port + max_attempts):
            if self.check_port_available(port):
                print(f"# Found available port: {port}")
                return port
        print(f"# No available port found in range {start_port}-{start_port + max_attempts - 1}")
        return None
    
    def wait_for_tor_connection(self, timeout=60):
        """Waits until Tor is ready to operate"""
        print("# Waiting for Tor to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                with Controller.from_port(port=self.control_port) as controller:
                    controller.authenticate()
                    print("# Control connection to Tor is working")
                    return True
            except Exception as e:
                print(f"# Waiting for Tor... ({int(time.time() - start_time)}s)")
                time.sleep(2)
        
        print("# Timeout - Tor is not responding")
        return False
    
    def find_tor_path(self):
        """Attempts to find the path to Tor.exe"""
        possible_paths = [
            r".\tor.exe",
            r"C:\Users\{}\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe".format(os.getenv('USERNAME')),
            r"C:\Program Files\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
            r"C:\Users\{}\Downloads\tor-win32-0.4.7.13\Tor\tor.exe".format(os.getenv('USERNAME')),
            "tor.exe"
        ]
        
        for path in possible_paths:
            if os.path.isfile(path):
                print(f"# Found Tor: {path}")
                return path
        return None
    
    def start_tor(self):
        """Starts the Tor process with configuration"""
        if not self.tor_path:
            self.tor_path = self.find_tor_path()
            
        if not self.tor_path:
            error_msg = "tor.exe not found! "
            print(f"# {error_msg}")
            sys.exit(1)
            
        try:
            tor_dir = os.path.dirname(self.tor_path)
            
            tor_config = f"""
SOCKSPort {self.socks_port}
ControlPort {self.control_port}
DataDirectory {tor_dir}\\Data
Log notice file {tor_dir}\\tor_log.txt
"""
            config_path = os.path.join(tor_dir, "torrc_temp")
            with open(config_path, "w") as f:
                f.write(tor_config)
            
            print(f"# Starting Tor on port: {self.socks_port}")
            
            self.tor_process = subprocess.Popen([
                self.tor_path, "-f", config_path
            ], cwd=tor_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if not self.wait_for_tor_connection():
                error_msg = "Tor did not start properly within the required time"
                print(f"# {error_msg}")
                self.stop()
                return False
                
            print("# Tor has been started and is ready")
            return True
            
        except Exception as e:
            error_msg = f"Error starting Tor: {e}"
            print(f"# {error_msg}")
            return False
    
    def get_current_ip(self, retries=3):
        """Checks current IP through Tor proxy with several attempts"""
        for attempt in range(retries):
            try:
                session = requests.Session()
                session.proxies = {
                    'http': f'socks5://127.0.0.1:{self.socks_port}',
                    'https': f'socks5://127.0.0.1:{self.socks_port}'
                }
                session.timeout = 30
                
                services = [
                    'http://httpbin.org/ip',
                    'https://api.ipify.org?format=json',
                    'http://icanhazip.com',
                    'https://ident.me'
                ]
                
                for service in services:
                    try:
                        response = session.get(service, timeout=15)
                        
                        if service == 'https://api.ipify.org?format=json':
                            return response.json()['ip']
                        elif service == 'http://httpbin.org/ip':
                            return response.json()['origin']
                        else:
                            return response.text.strip()
                            
                    except Exception as e:
                        continue
                
            except Exception as e:
                print(f"# Error checking IP (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(5)
        
        return None
    
    def change_tor_ip(self):
        """Changes IP by resetting the Tor circuit"""
        try:
            print("# Changing IP address...")
            
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                time.sleep(10)
                
                new_ip = self.get_current_ip()
                if new_ip:
                    print(f"# New IP: {new_ip}")
                else:
                    print("# Failed to check new IP address")
                    
        except Exception as e:
            print(f"# Error changing IP: {e}")
    
    def rotation_worker(self):
        """Thread for regular IP rotation"""
        while self.is_running:
            time.sleep(self.rotation_interval)
            if self.is_running:
                self.change_tor_ip()
    
    def start(self):
        """Starts the proxy and IP rotation"""
        print("")
        print("")
        print("")
        print("# Starting Tor Proxy Rotator...")
        
        # Check and find available port if needed
        if not self.check_port_available(self.socks_port):
            print(f"# Port {self.socks_port} is occupied, looking for available port...")
            new_port = self.find_available_port(9052)
            if new_port:
                self.socks_port = new_port
            else:
                print("# Could not find available port")
                return
        
        if not self.check_port_available(self.control_port):
            print(f"# Control port {self.control_port} is occupied, looking for available port...")
            new_control_port = self.find_available_port(9053)
            if new_control_port:
                self.control_port = new_control_port
            else:
                print("# Could not find available control port")
                return
        
        self.is_running = True
        
        if not self.start_tor():
            return
        
        print("# Testing connection...")
        initial_ip = self.get_current_ip()
        if initial_ip:
            print(f"# Initial IP: {initial_ip}")
        else:
            print("# Failed to check IP")
        
        rotation_thread = threading.Thread(target=self.rotation_worker)
        rotation_thread.daemon = True
        rotation_thread.start()
        
        print(f"\n# Your SOCKS5 Proxy: localhost:{self.socks_port}")
        print(f"# IP rotation every {self.rotation_interval} seconds")
        print("# Press Ctrl+C to stop")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stops the proxy"""
        print("\n# Stopping...")
        self.is_running = False
        if self.tor_process:
            self.tor_process.terminate()
            try:
                self.tor_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.tor_process.kill()
        print("# Stopped")

if __name__ == "__main__":
    # RECOMMENDED CONFIGURATION:
    SOCKS_PORT = 9052      # Recommended port (safe and rarely used)
    CONTROL_PORT = 9051    # Control port
    ROTATION_INTERVAL = 10 # Time between IP changes, specified in seconds
    
    TOR_PATH = None
    TOR_PATH = ".\\TOR\\tor\\tor.exe" # Path to tor.exe file - Pay attention to backslashes \\
    TOR_PATH = ".\\tor.exe" # Path to tor.exe file - Pay attention to backslashes \\
    
    rotator = TorProxyRotator(
        socks_port=SOCKS_PORT,
        control_port=CONTROL_PORT,
        rotation_interval=ROTATION_INTERVAL,
        tor_path=TOR_PATH
    )
    
    rotator.start()