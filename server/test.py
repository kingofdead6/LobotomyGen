import requests
import os
from urllib.parse import quote

# Configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_PHRASE = "I want to go to the gym."

def run_lobotomy_test():
    print(f"--- INITIALIZING LOBOTOMY TEST ---")
    print(f"Input: {TEST_PHRASE}\n")

    try:
        # Health check
        health = requests.get(f"{BASE_URL}/health")
        if health.status_code != 200:
            print(f"Health Check Failed: {health.status_code}")
            return

        # 1. Test Text Transformation
        response = requests.post(
            f"{BASE_URL}/transform",
            json={"message": TEST_PHRASE},
            timeout=60
        )

        if response.status_code != 200:
            print(f"Transform Error: {response.status_code} - {response.text}")
            return

        data = response.json()
        transformed_text = data["transformed"]
        voice_url = data["voice_api_url"]

        print(f"TRANSFORMED OUTPUT:\n{transformed_text}\n")
        print(f"Voice URL Generated: {BASE_URL}{voice_url}\n")

        # 2. Test Voice Generation (use POST for longer texts)
        print("--- GENERATING AUDIO ---")
        audio_response = requests.post(
            f"{BASE_URL}/voice",
            json={"text": transformed_text},
            timeout=120
        )

        if audio_response.status_code == 200:
            file_name = "lobotomy_output.mp3"
            with open(file_name, "wb") as f:
                f.write(audio_response.content)
            print(f"SUCCESS! Audio saved as: {os.path.abspath(file_name)}")
            print(f"Size: {len(audio_response.content) / 1024:.2f} KB")
        else:
            print(f"Failed to retrieve audio: {audio_response.status_code} - {audio_response.text}")

    except requests.exceptions.ConnectionError:
        print("CRITICAL ERROR: Is the server running? Could not connect.")
    except Exception as e:
        import traceback
        print(f"Test crashed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run_lobotomy_test()