import re
from collections import defaultdict

def detect_bruteforce(logfile, threshold=5):
    # Dictionary to hold IP addresses and their corresponding failed login counts
    ip_counts = defaultdict(int)
    
    # Regular expression to match SSHD failed login lines and capture the IP address
    pattern = re.compile(r'sshd.*Failed password.*from (\d+\.\d+\.\d+\.\d+)')
    
    with open(logfile, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                ip_counts[ip] += 1
                
    # Filter and return IPs that exceed the threshold
    brute_force_ips = [ip for ip, count in ip_counts.items() if count >= threshold]
    return brute_force_ips

# Usage
logfile = "/var/log/auth.log"
threshold = 5  # Change this value as per your requirements
suspicious_ips = detect_bruteforce(logfile, threshold)

if suspicious_ips:
    print("Potential brute-force attempts detected from the following IPs:")
    for ip in suspicious_ips:
        print(ip)
else:
    print("No brute-force attempts detected.")


