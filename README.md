# qBittorrent Port Updater

This project contains a Python script (`qbittorrent_port_updater.py`) that detects the forwarded port from a WireGuard VPN (e.g., ProtonVPN) using `port-checker.py` and updates the qBittorrent listening port to match it. The script runs in a loop, checking the port every 45 seconds and updating qBittorrent if necessary. This README provides instructions for setting up and running the script on **Windows**.

## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.x**: Version 3.9 or later recommended.
- **qBittorrent**: Installed with the Web UI enabled.
- **WireGuard VPN**: Configured with NAT-PMP or port forwarding enabled (e.g., ProtonVPN).
- **port-checker.py**: A script that detects the forwarded VPN port and outputs `The forwarded port is: <port>`.

## Installation on Windows

Follow these steps to install the dependencies and run the script on Windows.

### 1. Install Python
1. **Download Python**:
   - Visit [python.org](https://www.python.org/downloads/windows/) or install via the Microsoft Store.
   - Choose Python 3.9 or later (e.g., Python 3.11).
2. **Install Python**:
   - Run the installer.
   - Check the box for **"Add Python to PATH"** during installation.
   - Verify installation by opening a Command Prompt or PowerShell and running:
     ```
     python --version
     ```
     You should see the Python version (e.g., `Python 3.11.0`).
3. **Alternative Command**:
   - If `python` doesn’t work, try `py` or `python3`. The script uses `sys.executable` to handle this automatically.

### 2. Install Required Python Libraries
The script requires the `requests` library. The `configparser` and `pathlib` libraries are included in Python’s standard library.

1. Open a Command Prompt or PowerShell.
2. Install `requests` using pip:
   ```
   pip install requests
   ```
3. Verify installation:
   ```
   pip show requests
   ```
   You should see details about the installed `requests` package.

### 3. Install natpmpc (Optional)
The script calls `natpmpc` to renew NAT-PMP mappings, but this step is only required if your `port-checker.py` script depends on `natpmpc`. If `port-checker.py` detects the port independently (e.g., via a VPN API), you can skip this step.

1. **Download libnatpmp**:
   - Visit [miniupnp.free.fr](http://miniupnp.free.fr/libnatpmp.html) and download the `libnatpmp` source code.
2. **Compile natpmpc**:
   - Install a C compiler like [MinGW](http://www.mingw.org/) or [MSYS2](https://www.msys2.org/).
   - In MSYS2, install dependencies:
     ```
     pacman -S mingw-w64-x86_64-gcc
     ```
   - Extract the `libnatpmp` source, navigate to the directory, and compile:
     ```
     make
     ```
   - This generates `natpmpc.exe`.
3. **Add natpmpc to PATH**:
   - Copy `natpmpc.exe` to the same directory as `qbittorrent_port_updater.py` or to a directory in your system’s PATH (e.g., `C:\Windows`).
   - To add to PATH:
     - Search for “Environment Variables” in Windows.
     - Edit the “Path” variable in “System Variables” or “User Variables” and add the directory containing `natpmpc.exe`.
   - Verify by running:
     ```
     natpmpc
     ```
     If it runs without a “command not found” error, it’s correctly installed.
4. **Alternative**:
   - If `port-checker.py` handles port detection without `natpmpc` (e.g., using a VPN API), you don’t need `natpmpc`. The script will log a warning if `natpmpc` is missing but continue if `port-checker.py` works.

### 4. Set Up qBittorrent
1. **Install qBittorrent**:
   - Download and install qBittorrent from [qbittorrent.org](https://www.qbittorrent.org/download).
2. **Enable Web UI**:
   - Open qBittorrent and go to `Tools > Preferences > Web UI`.
   - Check “Enable the Web UI”.
   - Note the host (e.g., `http://localhost:8080`), username, and password.
   - Ensure qBittorrent is running when you execute the script.
3. **Test Web UI Access**:
   - Open a browser and navigate to the Web UI (e.g., `http://localhost:8080`).
   - Log in with your username and password to confirm it’s working.

### 5. Set Up port-checker.py
- Ensure `port-checker.py` is in the same directory as `qbittorrent_port_updater.py`.
- Verify it works on Windows by running:
  ```
  python port-checker.py
  ```
- It should output something like `The forwarded port is: 60661`.
- If `port-checker.py` uses `natpmpc`, ensure `natpmpc.exe` is installed (see step 3).
- If it uses a VPN API or another method, confirm your VPN client is running and configured for port forwarding.

### 6. Configure the VPN
- Ensure your VPN (e.g., ProtonVPN) is installed and running on Windows.
- Enable NAT-PMP or port forwarding in the VPN client settings (refer to your VPN’s documentation).
- Test port forwarding by running `port-checker.py` while connected to the VPN.

## Running the Script
1. **Place Scripts**:
   - Save `qbittorrent_port_updater.py` and `port-checker.py` in a directory (e.g., `C:\Users\YourName\wg-port-checker`).
2. **Run the Script**:
   - Open Command Prompt or PowerShell and navigate to the directory:
     ```
     cd C:\Users\YourName\wg-port-checker
     ```
   - Run the script:
     ```
     python qbittorrent_port_updater.py
     ```
   - If `python` doesn’t work, try:
     ```
     py qbittorrent_port_updater.py
     ```
3. **First Run**:
   - If no `.env` file exists, the script will prompt for qBittorrent’s Web UI host, username, and password.
   - These are saved to `.env` for future runs.
   - To reset credentials, delete the `.env` file and rerun the script.
4. **Expected Behavior**:
   - The script checks the VPN’s forwarded port every 45 seconds using `port-checker.py`.
   - It compares the forwarded port to qBittorrent’s current port and updates qBittorrent if they differ.
   - Logs show timestamps, detected ports, qBittorrent’s port, and update results.

## Example Output
```
This script uses port-checker.py to detect the forwarded WireGuard port and updates qBittorrent.
Ensure port-checker.py is in the same directory and you are connected to the VPN.
Loaded credentials from .env file.
Running in loop to renew the port every 45 seconds. Press Ctrl+C to stop.

[2025-10-24 15:45:00] Starting new loop iteration
[2025-10-24 15:45:00] natpmpc not found. Ensure it is installed or verify port-checker.py handles port detection independently.
[2025-10-24 15:45:00] Detected forwarded port: 60661
[2025-10-24 15:45:00] Current qBittorrent port: 12345
[2025-10-24 15:45:00] Port mismatch detected. Forwarded port: 60661, qBittorrent port: 12345
[2025-10-24 15:45:00] Successfully set qBittorrent listening port to 60661
[2025-10-24 15:45:00] qBittorrent port updated from 12345 to 60661
```

## Troubleshooting
1. **port-checker.py Fails**:
   - Run `python port-checker.py` to verify it outputs `The forwarded port is: <port>`.
   - If it depends on `natpmpc`, ensure `natpmpc.exe` is installed and in PATH.
   - Check VPN settings for port forwarding.

2. **qBittorrent Errors**:
   - If you see `qBittorrent login failed` or `Error communicating with qBittorrent`, verify:
     - qBittorrent Web UI is enabled and running.
     - Host, username, and password in `.env` are correct.
     - Delete `.env` and rerun to re-prompt for credentials.

3. **natpmpc Not Found**:
   - If `port-checker.py` doesn’t require `natpmpc`, ignore the warning.
   - Otherwise, install `natpmpc` as described in step 3 or modify `port-checker.py` to use a VPN API.

4. **VPN Issues**:
   - Ensure the VPN is connected and NAT-PMP/port forwarding is enabled.
   - Test with `port-checker.py` or manually run `natpmpc -g 10.2.0.1 -a 1 0 udp 60` (if installed).

5. **Python Command Issues**:
   - If `python` fails, try `py` or `python3`.
   - Verify Python is in PATH by running `python --version`.

## Notes
- **Security**: The `.env` file stores qBittorrent credentials in plain text. Keep it secure and exclude it from version control (e.g., add `.env` to `.gitignore`).
- **VPN Port Stability**: Some VPNs (e.g., ProtonVPN) may reuse the same port unless the connection resets. The script checks qBittorrent’s port every iteration to handle external changes.
- **Modifications**: If `port-checker.py` handles port detection without `natpmpc`, you can remove the `renew_natpmp_mapping()` call in the script by commenting it out:
  ```python
  # renew_natpmp_mapping()  # Skipped, assuming port-checker.py handles port detection
  ```

For further assistance, share the console output and details about your setup (e.g., VPN provider, qBittorrent version, Python version).
