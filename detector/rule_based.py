
from collections import defaultdict

def detect_bruteforce(events, threshold=5):
    ip_attempts = defaultdict(int)

    alerts = []

    for event in events:
        ip_attempts[event["ip"]] +=1
        if ip_attempts[event["ip"]] == threshold:
            alerts.append(event["ip"])

    return set(alerts)

