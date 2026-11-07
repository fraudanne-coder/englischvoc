import os
import pandas as pd
import requests

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "nDJIICjR9zfJExIFeSCN" # Emmaline Young (British girl)

if not API_KEY:
    print("Fehler: ELEVENLABS_API_KEY Secret nicht gefunden!")
    exit(1)

if not os.path.exists("vokabeln.csv"):
    print("vokabeln.csv nicht gefunden.")
    exit(1)

df = pd.read_csv("vokabeln.csv")
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

new_count = 0
for index, row in df.iterrows():
    word = str(row['en']).strip()
    safe_filename = "".join([c if c.isalnum() else "_" for c in word.lower()])
    while "__" in safe_filename: safe_filename = safe_filename.replace("__", "_")
    safe_filename = safe_filename.strip("_") + ".mp3"
    
    if os.path.exists(safe_filename):
        continue
        
    data = {
        "text": word,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    print(f"Generiere neue MP3: '{word}' -> {safe_filename}")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(safe_filename, "wb") as f:
            f.write(response.content)
        new_count += 1
    else:
        print(f"Fehler bei '{word}': {response.status_code}")

print(f"Fertig! {new_count} neue Audiodateien generiert.")
