import json
import time
import socket
import urllib.request

PI_IP = "192.168.0.120"
URL = f"http://{PI_IP}:5000/data"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except:
        return None

def get_battery():
    try:
        with open("/sys/class/power_supply/BAT0/capacity") as f:
            percent = int(f.read().strip())
        with open("/sys/class/power_supply/BAT0/status") as f:
            status = f.read().strip()
        return {"percent": percent, "charging": status}
    except:
        return None

def get_network():
    with open("/proc/net/dev") as f:
        lines = f.readlines()[2:]

    for line in lines:
        if "wlan" in line or "eth" in line:
            parts = line.split()
            return {
                "bytes_recv": int(parts[1]),
                "bytes_sent": int(parts[9])
            }
    return {}

def send(data):
    req = urllib.request.Request(
        URL,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)

while True:
    payload = {
        "hostname": socket.gethostname(),
        "cpu_temp": get_cpu_temp(),
        "battery": get_battery(),
        "network": get_network()
    }

    try:
        send(payload)
    except Exception as e:
        print("error:", e)

    time.sleep(10)
