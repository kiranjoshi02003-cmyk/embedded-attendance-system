import requests
import time

# Configuration
SERVER_URL = "http://127.0.0.1:5000/api/attendance"
MAC_ADDRESS = "AA:BB:CC:DD:EE:FF"

# This Base64 string must be the SAME as the one used in add_stud.py
FAKE_TEMPLATE = "SGVsbG8gYmlvc3luYyBwcm8hIFRoaXMgaXMgYSBzYW1wbGUgYmlvbWV0cmljIHRlbXBsYXRlIGJsb2IgZ2VuZXJhdGVkIGZvciB0ZXN0aW5nIHB1cnBvc2VzIGFuZCBzZWN1cml0eSB2YWxpZGF0aW9uIGluIHlvdXIgc3lzdGVtLiBUaGlzIHN0cmluZyBjYW4gYmUgZGVjb2RlZCBpbnRvIGJpbmFyeSBkYXRhIGZvciBTZXJ2ZXItU2lkZSBNYXRjaGluZy4="

def simulate_scan():
    payload = {
        "template_data": FAKE_TEMPLATE,
        "mac_address": MAC_ADDRESS,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload)
        # Printing the server response to see 'success' or 'error'
        print(f"Response from Server: {response.json()}")
    except Exception as e:
        print(f"Error: Could not connect to server: {e}")

# Run simulation
print("Hardware Simulator Started...")
while True:
    simulate_scan()
    time.sleep(5)