import subprocess
import re
import requests
import time
from pathlib import Path
import configparser
from datetime import datetime
import sys

# Path to .env file
ENV_FILE = Path('.env')

def load_env():
    """Load qBittorrent settings from .env file if it exists."""
    config = configparser.ConfigParser()
    if ENV_FILE.exists():
        config.read(ENV_FILE)
        if 'qBittorrent' in config:
            return (config['qBittorrent'].get('QB_HOST', 'http://localhost:8080'),
                    config['qBittorrent'].get('QB_USERNAME', 'admin'),
                    config['qBittorrent'].get('QB_PASSWORD', 'adminadmin'))
    return None

def save_env(host, username, password):
    """Save qBittorrent settings to .env file."""
    config = configparser.ConfigParser()
    config['qBittorrent'] = {
        'QB_HOST': host,
        'QB_USERNAME': username,
        'QB_PASSWORD': password
    }
    with ENV_FILE.open('w') as f:
        config.write(f)

def prompt_for_credentials():
    """Prompt user for qBittorrent credentials and save to .env."""
    print("Please provide qBittorrent Web UI settings:")
    host = input("Enter qBittorrent host (e.g., http://localhost:8080): ").strip() or 'http://localhost:8080'
    username = input("Enter qBittorrent username: ").strip() or 'admin'
    password = input("Enter qBittorrent password: ").strip() or 'adminadmin'
    save_env(host, username, password)
    return host, username, password

def get_forwarded_port():
    """Run port-checker.py to detect the forwarded port."""
    try:
        result = subprocess.run([sys.executable, 'port-checker.py'], capture_output=True, text=True, check=True)
        output = result.stdout
        match = re.search(r'The forwarded port is: (\d+)', output)
        if match:
            port = int(match.group(1))
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Detected forwarded port: {port}")
            return port
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Could not find mapped port in port-checker.py output: {output}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error running port-checker.py: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] port-checker.py not found. Ensure it is in the same directory.")
        return None

def renew_natpmp_mapping():
    """Explicitly renew NAT-PMP mapping for UDP."""
    try:
        result = subprocess.run(['natpmpc', '-g', '10.2.0.1', '-a', '1', '0', 'udp', '60'], capture_output=True, text=True, check=True)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NAT-PMP mapping renewed successfully: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error renewing NAT-PMP mapping: {e.stderr}")
    except FileNotFoundError:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] natpmpc not found. Ensure it is installed or verify port-checker.py handles port detection independently.")

def set_qbittorrent_port(port, host, username, password):
    """Set the listening port in qBittorrent."""
    session = requests.Session()
    login_url = f"{host}/api/v2/auth/login"
    try:
        response = session.post(login_url, data={'username': username, 'password': password}, timeout=10)
        if response.text != "Ok.":
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] qBittorrent login failed. Check username/password.")
            return False

        set_url = f"{host}/api/v2/app/setPreferences"
        data = {'json': f'{{"listen_port": {port}}}'}
        response = session.post(set_url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Successfully set qBittorrent listening port to {port}")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to set qBittorrent port. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error communicating with qBittorrent: {e}")
        return False

def get_current_qbittorrent_port(host, username, password):
    """Get the current listening port from qBittorrent."""
    session = requests.Session()
    login_url = f"{host}/api/v2/auth/login"
    try:
        response = session.post(login_url, data={'username': username, 'password': password}, timeout=10)
        if response.text != "Ok.":
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] qBittorrent login failed. Check username/password.")
            return None

        prefs_url = f"{host}/api/v2/app/preferences"
        response = session.get(prefs_url, timeout=10)
        if response.status_code == 200:
            prefs = response.json()
            current_port = prefs.get('listen_port')
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Current qBittorrent port: {current_port}")
            return current_port
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to get qBittorrent preferences. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error communicating with qBittorrent: {e}")
        return None

if __name__ == "__main__":
    print("This script uses port-checker.py to detect the forwarded WireGuard port and updates qBittorrent.")
    print("Ensure port-checker.py is in the same directory and you are connected to the VPN.")

    # Load or prompt for credentials
    credentials = load_env()
    if credentials is None:
        print("No .env file found or invalid. Prompting for credentials.")
        QB_HOST, QB_USERNAME, QB_PASSWORD = prompt_for_credentials()
    else:
        QB_HOST, QB_USERNAME, QB_PASSWORD = credentials
        print("Loaded credentials from .env file.")

    print("Running in loop to renew the port every 45 seconds. Press Ctrl+C to stop.")

    try:
        while True:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting new loop iteration")
            # Renew NAT-PMP mapping to ensure fresh port
            renew_natpmp_mapping()
            
            # Get the forwarded port
            port = get_forwarded_port()
            if port:
                # Always check the current qBittorrent port
                current_qb_port = get_current_qbittorrent_port(QB_HOST, QB_USERNAME, QB_PASSWORD)
                if current_qb_port is None:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Skipping port update due to failure in retrieving current qBittorrent port.")
                elif current_qb_port != port:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Port mismatch detected. Forwarded port: {port}, qBittorrent port: {current_qb_port}")
                    if set_qbittorrent_port(port, QB_HOST, QB_USERNAME, QB_PASSWORD):
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] qBittorrent port updated from {current_qb_port} to {port}")
                    else:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to update qBittorrent port.")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No change needed: qBittorrent port ({current_qb_port}) matches forwarded port ({port}).")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Failed to detect forwarded port. Retrying in 45 seconds.")
            time.sleep(45)
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Stopped.")