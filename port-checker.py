import subprocess
import re

def get_forwarded_port():
    try:
        # Run natpmpc to request/renew the port mapping for UDP
        result = subprocess.run(['natpmpc', '-g', '10.2.0.1', '-a', '1', '0', 'udp', '60'], capture_output=True, text=True, check=True)
        output = result.stdout
        match = re.search(r'Mapped public port (\d+)', output)
        if match:
            return int(match.group(1))
        else:
            print("Could not find mapped port in output:", output)
            return None
    except subprocess.CalledProcessError as e:
        print("Error running natpmpc:", e)
        return None
    except FileNotFoundError:
        print("natpmpc not found. Please install it (e.g., sudo apt install natpmpc on Debian/Ubuntu).")
        return None

if __name__ == "__main__":
    print("This script assumes you are using ProtonVPN with WireGuard and NAT-PMP enabled.")
    print("Ensure you are connected to the VPN and natpmpc is installed.")
    
    forwarded_port = get_forwarded_port()
    if forwarded_port:
        print(f"The forwarded port is: {forwarded_port}")
    else:
        print("Failed to detect the forwarded port.")