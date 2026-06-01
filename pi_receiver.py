from flask import Flask, request
import json
from collections import deque
from datetime import datetime

app = Flask(__name__)

last_100 = deque(maxlen=100)

def add_timestamp(data):
    return {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

@app.route('/data', methods=['POST'])
def receive_data():
    raw = request.json

    entry = add_timestamp(raw)

    
    print(json.dumps(entry, indent=2))

    # full log
    with open("/home/rohan/Downloads/log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

    # rolling last 100 entries
    last_100.append(entry)

    with open("/home/rohan/Downloads/laptop_stats.json", "w") as f:
        json.dump(list(last_100), f, indent=2)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)