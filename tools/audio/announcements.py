import yaml
import os
import wave
from google import genai
from google.genai import types

MODEL="gemini-2.5-pro-preview-tts"

client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def save_wave(filename,data):
    with wave.open(filename,"wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(data)

with open("tools/audio/announcements.yml") as f:
    cfg=yaml.safe_load(f)

voice=cfg["voice"]

for ann in cfg["announcements"]:

    for lang,text in ann["text"].items():

        path=ann["audio"][lang]

        if text.startswith("("):
            continue

        os.makedirs(os.path.dirname(path),exist_ok=True)

        print("Generating",ann["id"],lang)

        r=client.models.generate_content(
            model=MODEL,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice
                        )
                    )
                )
            )
        )

        pcm=r.candidates[0].content.parts[0].inline_data.data

        save_wave(path,pcm)