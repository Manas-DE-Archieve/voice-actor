import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ========================
# CONFIG
# ========================
TTS_API_URL = os.getenv("TTS_API_URL")
ASR_API_URL = os.getenv("ASR_API_URL")

TTS_TOKEN = os.getenv("TTS_TOKEN")
ASR_TOKEN = os.getenv("ASR_TOKEN")


# ========================
# TEXT → SPEECH
# ========================
def text_to_speech(text: str, output_file: str = "voice.mp3"):
    headers = {
        "Authorization": f"Bearer {TTS_TOKEN}",
        "Content-Type": "application/json",
        "Origin": "https://tts.aitil.kg",
        "Referer": "https://tts.aitil.kg/",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "text": text,
        "speaker_id": "2"
    }

    response = requests.post(TTS_API_URL, json=payload, headers=headers)

    if response.ok:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print("✅ TTS готов:", output_file)
        return output_file
    else:
        print("❌ TTS ошибка:", response.status_code, response.text)
        return None


# ========================
# SPEECH → TEXT
# ========================
def speech_to_text(file_path: str):
    headers = {
        "x-api-token": ASR_TOKEN,
        "Origin": "https://asr.aitil.kg",
        "Referer": "https://asr.aitil.kg/"
    }

    with open(file_path, "rb") as f:
        files = {
            "file": (file_path, f, "audio/mpeg")
        }

        response = requests.post(ASR_API_URL, headers=headers, files=files)

    if response.ok:
        data = response.json()
        print("✅ ASR текст:", data)
        return data
    else:
        print("❌ ASR ошибка:", response.status_code, response.text)
        return None


# ========================
# PIPELINE
# ========================
if __name__ == "__main__":
    audio = text_to_speech("кандайсын")

    if audio:
        speech_to_text(audio)