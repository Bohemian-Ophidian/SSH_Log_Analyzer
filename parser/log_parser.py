import subprocess
import re

FAILED_PATTERN = re.compile(r'Failed password for (?:invalid user |user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)')

def parse_ssh_journal():
    cmd = ["journalctl", "-u", "ssh", "--no-pager"]
    output = subprocess.check_output(cmd, text=True)

    events = []

    for line in output.splitlines():
        m = FAILED_PATTERN.search(line)
        if m:
            events.append({
                "ip": m.group("ip"),
                "user": m.group("user"),
                "status": "FAILED"
                })
    return events
