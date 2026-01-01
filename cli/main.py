import argparse
from parser.log_parser import parse_ssh_journal
from detector.rule_based import detect_bruteforce
from detector.feature_extractor import extract_features
from detector.ml_detector import detect_anomalies 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=False)
    args = parser.parse_args()

    events = parse_ssh_journal()

    brute_ips = detect_bruteforce(events)
    X, ips = extract_features(events)
    anomalies = detect_anomalies(X)

    for ip, pred in zip(ips, anomalies):
        if ip in brute_ips or pred == -1:
            print(f"**Warning ** malicious activity detected from {ip}")

if __name__ == "__main__":
    main()
