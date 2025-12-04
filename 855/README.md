# Desire - HackTheBox Challenge Walkthrough

A comprehensive walkthrough of the **Desire** web challenge from HackTheBox, demonstrating how to chain a logic flaw with a Zip Slip vulnerability to bypass authentication and achieve admin access.

**Category:** Web | **Difficulty:** Easy (arguably Medium)

📖 **Full Writeup:** [Read on Medium](https://thehackboy.medium.com/exploiting-logic-flaws-zip-slips-a-walkthrough-of-desires-on-hack-the-box-c68a39eea650?postPublishedType=initial)

---

## Challenge Overview

The Desire application uses a microservices architecture with:
- **Frontend (Go):** Handles HTTP requests and file uploads
- **Backend (Node.js/SSO):** Manages authentication and database
- **Redis:** Session storage (prime target for exploitation)

---

## Vulnerabilities Identified

### 1. **Logic Flaw (Race Condition)**
**Location:** `challenge/service/services/http.go` - LoginHandler

The authentication flow performs operations in the wrong order:
1. `PrepareSession()` - Creates Redis session entry BEFORE verifying credentials
2. `loginUser()` - Verifies password ONLY AFTER session creation

**Impact:** Even with an incorrect password, a valid Redis session remains, bypassing Redis validation checks.

### 2. **Zip Slip (CVE-2024-0406)**
**Location:** `challenge/service/go.mod` - archiver v3.5.0

The vulnerable archiver library allows arbitrary file writes via:
- Directory traversal characters (`../../`) in archive paths
- Symlink exploitation during extraction

**Impact:** Write malicious session files to `/tmp/sessions/<username>/<session_id>` by creating symlinks in uploaded archives.

---

## Exploitation Steps

### Step 1: Predict Session ID
```bash
python3 get_session_id.py http://target:port
```
- Extracts the `Date` header from a fake login response
- Calculates SHA256(Unix timestamp) to predict generated Session IDs
- Generates 3 potential Session IDs due to timing variations

### Step 2: Create Malicious Payload
```bash
python3 create_malicious_tar.py
```
- Generates `payload.tar` containing:
  - A symlink pointing to `/tmp/sessions`
  - Malicious JSON file with `"role":"admin"` for predicted Session IDs

### Step 3: Upload & Trigger
```bash
python3 upload_malicious_tar.py http://target:port
```
- Creates a normal user account
- Logs in successfully
- Uploads the malicious tar file
- The server extracts and follows the symlink, writing admin session files

### Step 4: Retrieve Flag
```bash
python3 KO.py http://target:port SESSION_ID_1 SESSION_ID_2 SESSION_ID_3
```
- Bypasses both validation checks:
  - Redis check: Passed (via Step 1 logic flaw)
  - Filesystem check: Passed (via Step 3 Zip Slip)
- Accesses `/user/admin` and extracts the flag

---

## Files Included

- `get_session_id.py` - Predict valid Session IDs based on server time
- `create_malicious_tar.py` - Generate Zip Slip payload
- `upload_malicious_tar.py` - Upload and trigger the exploit
- `KO.py` - Validate and retrieve the flag

---

## Key Lessons

1. **Order of Operations Matters:** Always validate credentials BEFORE creating session state
2. **Keep Dependencies Updated:** Zip Slip and similar vulnerabilities are well-documented
3. **Never Trust Partial State:** Session creation should be atomic or delayed until full verification
4. **Defense in Depth:** Relying on multiple checks (Redis + Filesystem) is good, but they must all pass before granting access

---

**Author:** Muhammad Younas | **Date:** December 2025