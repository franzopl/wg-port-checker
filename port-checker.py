import socket

def get_forwarded_port(gateway='10.2.0.1', protocol='udp', suggested_public_port=0, private_port=0, lifetime=60):
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

        return public_port
    except Exception as e:
        print(f"Error detecting forwarded port: {e}")
        return None
    finally:
        sock.close()

if __name__ == "__main__":
    print("This script assumes you are using ProtonVPN with WireGuard and NAT-PMP enabled.")
    print("Ensure you are connected to the VPN.")
    
    forwarded_port = get_forwarded_port()
    if forwarded_port:
        print(f"The forwarded port is: {forwarded_port}")
    else:
        print("Failed to detect the forwarded port.")