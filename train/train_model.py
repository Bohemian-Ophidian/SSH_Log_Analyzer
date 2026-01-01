#!/usr/bin/env python3

import re
import os
from collections import defaultdict
from sklearn.ensemble import IsolationForest
import joblib

FAILED_PATTERN = re.compile(
        r"Failed password for (?:invalid user |user)?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)"
        )

def parse_dummy_journal(path):
    events = []

    with open(path, "r") as f:
        for line in f:
            match = FAILED_PATTERN.search(line)
            if match:
                events.append({
                    "ip": match.group("ip"),
                    "user": match.group("user")
                })
    print(events)
    return events

def extract_features(events):
    stats = defaultdict(lambda: {
        "fail_count": 0,
        "users": set()
        })
    
    for e in events:
        stats[e["ip"]]["fail_count"] += 1
        stats[e["ip"]]["users"].add(e["user"])

    X, ips = [], []
    
    for ip, data in stats.items():
        X.append([
            data["fail_count"],
            len(data["users"])
            ])
        ips.append(ip)
    return X, ips

LOG_FILE = "train_logs/dummy_journal.log"
MODEL_PATH = "models/isolation_forest.pkl"

def main():
    events = parse_dummy_journal(LOG_FILE)

    X, ips = extract_features(events)

    model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
            )
    model.fit(X)

    os.makedirs("models", exist_ok = True)
    joblib.dump(model, MODEL_PATH)

    print(f" model trained and saved")
    print("IPs used during training:", ips)

if __name__ == "__main__":
    main()

