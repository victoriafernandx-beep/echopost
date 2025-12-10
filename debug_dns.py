import socket
import sys
import streamlit as st

def test_dns(hostname):
    print(f"Testing DNS for: {hostname}")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"[OK] Resolved to {ip}")
        return True
    except Exception as e:
        print(f"[FAIL] DNS Error: {e}")
        return False

try:
    url = "nqiaokjpdszfvehvprep.supabase.co"
    print(f"Checking derived URL: {url}")
    if not test_dns(url):
        print("Trying user provided version...")
        url_user = "nqiaokjpdszfuehvprep.supabase.co"
        test_dns(url_user)
except Exception as e:
    print(e)
