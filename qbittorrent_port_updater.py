import socket
import requests
import time
from pathlib import Path
import configparser
from datetime import datetime

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
    if ENV_FILE.exists():
        config.read(ENV_FILE)
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

def get_forwarded_port(gateway='10.2.0.1', protocol='udp', suggested_public_port=0, private_port=0, lifetime=60):
    """Detect the forwarded port using NAT-PMP."""
    if protocol.lower() == 'udp':
        op = 1
    elif protocol.lower() == 'tcp':
        op = 2
    else:
        raise ValueError("Protocol must be 'udp' or 'tcp'")

    # Build the request packet
    packet = bytes([0, op]) + bytes([0] * 2) + private_port.to_bytes(2, 'big') + suggested_public_port.to_bytes(2, 'big') + lifetime.to_bytes(4, 'big')

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Timeout for response

    try:
        # Send request to gateway on port 5351
        sock.sendto(packet, (gateway, 5351))

        # Receive response
        data, addr = sock.recvfrom(1024)

        # Parse response
        if len(data) < 16:
            raise Exception("Response too short")

        version = data[0]
        resp_op = data[1]
        result = int.from_bytes(data[2:4], 'big')
        epoch = int.from_bytes(data[4:8], 'big')
        returned_private_port = int.from_bytes(data[8:10], 'big')
        public_port = int.from_bytes(data[10:12], 'big')
        returned_lifetime = int.from_bytes(data[12:16], 'big')

        if version != 0 or resp_op != (128 + op):
            raise Exception("Invalid response format")

        if result != 0:
            raise Exception(f"NAT-PMP error code: {result}")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Detected forwarded port: {public_port}")
        return public_port
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error detecting forwarded port: {e}")
        return None
    finally:
        sock.close()

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
    print("This script detects the forwarded WireGuard port using NAT-PMP and updates qBittorrent.")
    print("Ensure you are connected to the VPN with NAT-PMP enabled (e.g., ProtonVPN).")

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