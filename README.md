# 📡 Laptop → Raspberry Pi System Monitor Logger

Stream system metrics from a laptop to a Raspberry Pi over a local network every 10 seconds. The Pi acts as a centralized logging node that stores and organizes incoming data.

Built with lightweight Python — no heavy external dependencies.

---

## Features

- Real-time system monitoring from laptop
- JSON-based data streaming over HTTP
- Raspberry Pi acts as a central log server
- Full history logging + rolling last 100 entries
- Timestamped data entries
- Works over local network (LAN/WiFi)

---

## Architecture

```
Laptop (Sender)
  └── Collects system data
  └── Sends JSON every 10 seconds via HTTP POST
        │
        ▼
Raspberry Pi (Receiver)
  └── Receives data via Flask server
  └── Prints live logs
  └── Stores full history + last 100 snapshots
```

---

## Data Collected

Each packet contains:

| Field | Description |
|---|---|
| `cpu_temp` | CPU temperature |
| `battery.percent` | Battery percentage |
| `battery.charging` | Charging status |
| `network.bytes_recv` | Network bytes received |
| `network.bytes_sent` | Network bytes sent |
| `hostname` | Device hostname |
| `timestamp` | Added by Pi on receipt |

---

## Setup

### 1. Raspberry Pi (Receiver)

Install Flask:

```bash
pip install flask
```

Run the server:

```bash
python3 pi_receiver.py
```

### 2. Laptop (Sender)

Run the sender script:

```bash
python3 sender.py
```

> No external libraries required — uses built-in Python modules only.

---

## File Storage (Pi)

| File | Description |
|---|---|
| `~/Downloads/log.jsonl` | Full log (append-only) |
| `~/Downloads/laptop_stats.json` | Rolling log (last 100 entries) |

---

## Example Data Format

```json
{
  "timestamp": "2026-06-01T17:10:25",
  "data": {
    "cpu_temp": 38.0,
    "battery": {
      "percent": 63,
      "charging": "Discharging"
    },
    "network": {
      "bytes_recv": 123456,
      "bytes_sent": 654321
    },
    "hostname": "laptop"
  }
}
```

---

## Notes

- Designed for **local network use only**
- Minimal dependency design (Flask only on Pi)
- Useful for learning IoT-style data pipelines
- Easily extended for dashboards or ML logging

---

## Future Improvements

- [ ] Web dashboard for live visualization
- [ ] Database storage (SQLite / InfluxDB)
- [ ] Multi-device support
- [ ] Graph plotting system
- [ ] Systemd service for auto startup
