import os
import sys
import codecs
from openai import OpenAI
from dotenv import load_dotenv

# Force UTF-8 for stdout/stderr to handle emojis on Windows
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Load environment variables
load_dotenv()

def verify_setup():
    print("🔍 Verifying OpenAI Setup for WhatsApp Bot...")
    
    # 1. Check API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("   Please create a .env file with OPENAI_API_KEY=your-key-here")
        return False
    
    print(f"✅ OPENAI_API_KEY found (starts with {api_key[:5]}...)")
    
    # 2. Check Client Initialization
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI Client initialized.")
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        return False

    # 3. Test Chat Completion
    print("\n🧪 Testing Chat Completion (GPT-4o-mini)...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Health check passed' if you can hear me."}
            ],
            max_tokens=20
        )
        content = response.choices[0].message.content
        print(f"✅ Chat Response: {content}")
    except Exception as e:
        print(f"❌ Error during chat completion: {e}")
        return False

    # 4. Test Audio Transcription (Mock check)
    # We won't upload a real file to save credits/complexity, 
    # but we will check if the client has the audio attribute accessible.
    print("\n🧪 Verifying Audio Capability...")
    if hasattr(client, 'audio') and hasattr(client.audio, 'transcriptions'):
       print("✅ Client has audio.transcriptions capability.")
    else:
       print("⚠️ Warning: Client might not support audio or library version mismatch.")
    
    print("\n✨ Setup verification completed successfully!")
    return True

if __name__ == "__main__":
    success = verify_setup()
    if not success:
        sys.exit(1)
