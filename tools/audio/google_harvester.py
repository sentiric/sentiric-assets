import os
import time
import wave
from google import genai
from google.genai import types

# --- AYARLAR ---
OUTPUT_BASE_DIR = "docs/audio/speakers"
API_KEY = os.environ.get("GEMINI_API_KEY")

# DOĞRU MODEL İSMİ
MODEL_NAME = "gemini-2.5-flash-preview-tts"
# MODEL_NAME = "gemini-2.5-pro-preview-tts"  # Alternatif

# Limitler: Dakikada 3 istek, Günde 15 istek (ücretsiz tier)
SAFE_DELAY = 60  # 60/3 = 20 + 5 saniye güvenlik
DAILY_LIMIT = 10

# --- GOOGLE TTS SES KADROSU (Dokümanda Listelenen 30 Ses) ---
# DÜZELTME NOTU (2025): 6 Sesin Cinsiyet Etiketi (Gender Label) düzeltildi.
VOICE_DB = {
    # --- TÜRKÇE KADROSU ---
    "Fenrir":   {"name": "M_TR_Heyecanli_Can", "lang": "tr", "gender": "M"},
    "Puck":     {"name": "M_TR_Enerjik_Mert",  "lang": "tr", "gender": "M"},
    "Kore":     {"name": "F_TR_Kurumsal_Ece",  "lang": "tr", "gender": "F"},
    "Leda":     {"name": "F_TR_Genc_Selin",    "lang": "tr", "gender": "F"},
    "Charon":   {"name": "M_TR_Tok_Kadir",     "lang": "tr", "gender": "M"},
    "Zephyr":   {"name": "F_TR_Parlak_Zeynep", "lang": "tr", "gender": "F"},
    
    # --- İNGİLİZCE KADROSU ---
    "Orus":         {"name": "M_EN_Corporate_Orus", "lang": "en"},
    "Aoede":        {"name": "F_EN_Elegant_Aoede",  "lang": "en"},
    "Callirrhoe":   {"name": "F_EN_Calm_Calli",     "lang": "en"},
    "Enceladus":    {"name": "M_EN_Breathless_Ence","lang": "en"},
    "Umbriel":      {"name": "M_EN_Adaptive_Umbriel","lang": "en"},
    
    # DÜZELTME 1: Algieba (F -> M)
    "Algieba":      {"name": "M_EN_Smooth_Algieba", "lang": "en"},
    
    "Despina":      {"name": "F_EN_Polished_Despina","lang": "en"},
    
    # DÜZELTME 2: Erinome (M -> F)
    "Erinome":      {"name": "F_EN_Clear_Erinome",  "lang": "en"},
    
    "Algenib":      {"name": "M_EN_Gravelly_Algenib","lang": "en"},
    
    # DÜZELTME 3: Rasalgethi (F -> M)
    "Rasalgethi":   {"name": "M_EN_Teacher_Rasal",  "lang": "en"},
    
    "Laomedeia":    {"name": "F_EN_Upbeat_Lao",     "lang": "en"},
    
    # DÜZELTME 4: Achernar (M -> F)
    "Achernar":     {"name": "F_EN_Soft_Achernar",  "lang": "en"},
    
    "Alnilam":      {"name": "M_EN_Firm_Alnilam",   "lang": "en"},
    "Schedar":      {"name": "M_EN_Even_Schedar",   "lang": "en"},
    
    # DÜZELTME 5: Gacrux (M -> F)
    "Gacrux":       {"name": "F_EN_Mature_Gacrux",  "lang": "en"},
    
    "Pulcherrima":  {"name": "F_EN_Eager_Pulcher",  "lang": "en"},
    "Achird":       {"name": "M_EN_Friendly_Achird","lang": "en"},
    "Zubenelgenubi":{"name": "M_EN_Casual_Zuben",   "lang": "en"},
    "Vindemiatrix": {"name": "F_EN_Gentle_Vindem",  "lang": "en"},
    
    # DÜZELTME 6: Sadachbia (F -> M)
    "Sadachbia":    {"name": "M_EN_Lively_Sadach",  "lang": "en"},
    
    "Sadaltager":   {"name": "M_EN_Wise_Sadal",     "lang": "en"},
    "Sulafat":      {"name": "F_EN_Warm_Sulafat",   "lang": "en"},
    "Autonoe":      {"name": "F_EN_Bright_Autonoe", "lang": "en"},
    "Iapetus":      {"name": "M_EN_Clear_Iapetus",  "lang": "en"}
}

# WAV dosyası kaydetme fonksiyonu
def save_wave_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Google'ın örnek kodundaki wave kaydetme fonksiyonu"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

# Duygu bazlı prompt'lar
PROMPTS = {
    "tr": {
        "neutral": "Bu, Sentiric platformu için oluşturulmuş standart bir ses testidir. Sistem normal çalışıyor.",
        "happy": "Say cheerfully: İnanılmaz! Bu proje harika gidiyor, sonuçları görünce çok mutlu oldum!",
        "sad": "Say in a sad tone: Maalesef işler planladığımız gibi gitmedi, bu durum beni biraz üzüyor.",
        "angry": "Say angrily: Bu kabul edilemez! Derhal bu hatanın düzeltilmesini istiyorum!",
        "whisper": "Say in a spooky whisper: Şşt, sessiz ol. Bu çok gizli bir bilgi, kimsenin duymaması lazım."
    },
    "en": {
        "neutral": "This is a standard voice test for the Sentiric platform. Systems are operational.",
        "happy": "Say cheerfully: Wow! This is absolutely amazing news, I am so excited to see the results!",
        "sad": "Say in a sad tone: I am sorry to hear that, it is very unfortunate and disappointing.",
        "angry": "Say angrily: I cannot believe you did that! It is completely unacceptable!",
        "whisper": "Say in a spooky whisper: Hush, keep your voice down. This is a secret."
    }
}

def generate_tts(client, voice_name, style, prompt_text, output_path):
    """Google TTS ile ses üret"""
    print(f"   🎙️  {style.upper()} üretiliyor...", end="", flush=True)
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                )
            )
        )
        
        if (response.candidates and 
            response.candidates[0].content and 
            response.candidates[0].content.parts):
            
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    save_wave_file(output_path, part.inline_data.data)
                    print(f" ✅")
                    return True
        
        print(f" ❌ Ses verisi bulunamadı")
        return False
        
    except Exception as e:
        error_msg = str(e)
        print(f" ❌ HATA: {error_msg[:100]}...")
        
        if "429" in error_msg or "quota" in error_msg.lower():
            import re
            match = re.search(r"retry in (\d+\.?\d*)s", error_msg.lower())
            if match:
                wait_time = float(match.group(1)) + 2
                print(f"   ⏳ {wait_time:.1f} saniye bekle...")
                time.sleep(wait_time)
            else:
                print(f"   ⏳ 30 saniye bekle...")
                time.sleep(30)
            
            try:
                return generate_tts(client, voice_name, style, prompt_text, output_path)
            except:
                return False
        
        elif "404" in error_msg:
            print(f"   🔴 MODEL BULUNAMADI: {MODEL_NAME}")
            return False
        
        return False

def check_available_models(client):
    """Mevcut modelleri listele"""
    print("\n🔍 Mevcut Modeller Kontrol Ediliyor...")
    try:
        models = client.models.list()
        print("📋 Mevcut Modeller:")
        tts_models = []
        for model in models:
            model_name = model.name.replace("models/", "")
            if "tts" in model_name.lower() or "flash" in model_name.lower() or "pro" in model_name.lower():
                tts_models.append(model_name)
                print(f"   📦 {model_name}")
        print(f"\n✅ Toplam {len(tts_models)} TTS modeli bulundu")
        return tts_models
    except Exception as e:
        print(f"❌ Model listeleme hatası: {e}")
        return []

def test_tts_model(client):
    """TTS modelinin çalıştığını test et"""
    print("\n🧪 TTS Model Testi...")
    test_voices = ["Fenrir", "Puck", "Kore"]
    for voice in test_voices:
        try:
            print(f"   Testing {voice}...", end="", flush=True)
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents="Say: Test",
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
            if response.candidates:
                print(f" ✅")
                return True
        except Exception as e:
            print(f" ❌ ({voice}): {str(e)[:80]}")
    return False

def main():
    if not API_KEY:
        print("🔴 HATA: GEMINI_API_KEY eksik.")
        print("ℹ️  Export yapın: export GEMINI_API_KEY='your-key-here'")
        return
    
    client = genai.Client(api_key=API_KEY)
    
    print(f"🚀 GOOGLE TTS HARVESTER BAŞLIYOR")
    print(f"ℹ️  Model: {MODEL_NAME}")
    print(f"ℹ️  Hız Limiti: {SAFE_DELAY} saniye/islek")
    print(f"ℹ️  Günlük Limit: {DAILY_LIMIT} istek")
    print(f"📂 Hedef: {os.path.abspath(OUTPUT_BASE_DIR)}\n")
    
    available_models = check_available_models(client)
    
    if MODEL_NAME not in available_models and "models/" + MODEL_NAME not in available_models:
        print(f"\n⚠️  UYARI: {MODEL_NAME} listede yok!")
        return
    
    if not test_tts_model(client):
        print("\n⚠️  TTS testi başarısız.")
        return
    
    print("\n✅ TTS modeli çalışıyor! Ses üretimine başlanıyor...\n")
    
    daily_count = 0
    total_tasks = len(VOICE_DB) * 5
    completed_tasks = 0
    
    for google_voice, info in VOICE_DB.items():
        sentiric_name = info['name']
        lang = info['lang']
        
        if daily_count >= DAILY_LIMIT:
            print(f"\n⚠️  GÜNLÜK LİMİT ({DAILY_LIMIT}) DOLDU!")
            break
        
        speaker_dir = os.path.join(OUTPUT_BASE_DIR, sentiric_name)
        if not os.path.exists(speaker_dir):
            os.makedirs(speaker_dir)
            print(f"📁 Klasör: {sentiric_name}")
        
        print(f"\n👤 İşleniyor: {google_voice} -> {sentiric_name} ({lang.upper()})")
        
        for style, prompt_text in PROMPTS[lang].items():
            completed_tasks += 1
            filename = f"{style}.wav"
            filepath = os.path.join(speaker_dir, filename)
            
            if os.path.exists(filepath):
                print(f"   ⏭️  {style} atlandı")
                continue
            
            success = generate_tts(client, google_voice, style, prompt_text, filepath)
            
            if success:
                daily_count += 1
                print(f"   📊 Günlük: {daily_count}/{DAILY_LIMIT}")
                if not (google_voice == list(VOICE_DB.keys())[-1] and 
                       style == list(PROMPTS[lang].keys())[-1]):
                    print(f"   ⏳ {SAFE_DELAY}sn bekleniyor...")
                    time.sleep(SAFE_DELAY)
            
            if daily_count >= DAILY_LIMIT:
                print(f"\n⚠️  GÜNLÜK LİMİT ({DAILY_LIMIT}) DOLDU!")
                break
        
        if daily_count >= DAILY_LIMIT:
            break
    
    print(f"\n✨ İŞLEMLER TAMAMLANDI!")
    print(f"   📈 Üretilen ses: {daily_count}/{DAILY_LIMIT}")
    print(f"   ✅ Tamamlanan görev: {completed_tasks}/{total_tasks}")

if __name__ == "__main__":
    main()