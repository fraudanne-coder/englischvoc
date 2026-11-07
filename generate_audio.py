import os
import pandas as pd
import requests

# Konfiguration
VOICE_ID = "nDJIICjR9zfJExIFeSCN"  # Emmaline Young
API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise ValueError("Fehler: ELEVENLABS_API_KEY Secret nicht gefunden!")

if not os.path.exists("vokabeln.csv"):
    raise FileNotFoundError("Die Datei vokabeln.csv wurde nicht gefunden.")

df = pd.read_csv("vokabeln.csv")

if "en" not in df.columns:
    raise ValueError("Die Spalte 'en' wurde in der vokabeln.csv nicht gefunden.")

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

for index, row in df.iterrows():
    word = str(row["en"]).strip()
    if not word or pd.isna(row["en"]):
        continue
        
    # Leerzeichen durch Unterstrich ersetzen, damit der Dateiname sauber ist
    safe_filename_base = word.replace(" ", "_")
    filename = f"{safe_filename_base}.mp3"
    
    if os.path.exists(filename):
        continue

    payload = {
        "text": word,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"Generiere neue MP3: '{word}' -> {filename}", flush=True)
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Erfolgreich gespeichert: {filename}", flush=True)
    else:
        print(f"Fehler bei '{word}': Statuscode {response.status_code} - Antwort: {response.text}", flush=True)

print("Fertig! Alle Audioprozesse abgeschlossen.", flush=True)
