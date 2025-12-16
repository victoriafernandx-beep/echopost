import requests
import json
import time
import sys
import codecs

# Force UTF-8 for stdout/stderr to handle emojis on Windows
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

BASE_URL = "http://localhost:5000/webhook"
VERIFY_TOKEN = "echopost_webhook_2024"

def test_verify_webhook():
    print("\n🧪 Testing Webhook Verification (GET)...")
    endpoint = BASE_URL
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': VERIFY_TOKEN,
        'hub.challenge': '123456789'
    }
    
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200 and response.text == '123456789':
            print("✅ Webhook verification successful!")
            return True
        else:
            print(f"❌ Webhook verification failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_receive_message():
    print("\n🧪 Testing Receive Message (POST)...")
    endpoint = BASE_URL
    
    # Mock WhatsApp Message Payload
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456789",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "123456789",
                        "phone_number_id": "123456789"
                    },
                    "contacts": [{
                        "profile": {"name": "Test User"},
                        "wa_id": "5511999999999"
                    }],
                    "messages": [{
                        "from": "5511999999999",
                        "id": "wamid.HBgLMTIzNDU2Nzg5AA==",
                        "timestamp": "1702409000",
                        "type": "text",
                        "text": {"body": "This is a test message for EchoPost"}
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        # Note: This will trigger the actual processing logic in app.py
        # which will try to call OpenAI.
        # It will ALSO try to send a message back via WhatsApp API, which will likely fail or log an error
        # because we don't have a valid valid recipient/token for the *sending* part in this simulated env
        # unless everything is perfectly mocked.
        # However, we mostly want to check if it returns 200 OK to the webhook.
        
        response = requests.post(endpoint, json=payload, headers=headers)
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Message processed successfully (200 OK)")
            return True
        else:
            print(f"❌ Message processing failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    if test_verify_webhook():
        test_receive_message()
