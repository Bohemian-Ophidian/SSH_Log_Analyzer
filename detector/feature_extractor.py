
from collections import defaultdict

def extract_features(events):
    features = defaultdict(lambda: {
        "fail_count": 0,
        "unique_users": set()
        })

    for e in events:
        ip = e["ip"]
        features[ip]["fail_count"] += 1
        features[ip]["unique_users"].add(e["user"])

    X = []
    ips = []

    for ip, data in features.items():
        X.append([
            data["fail_count"], 
            len(data["unique_users"])
            ])
        ips.append(ip)

    return X, ips
