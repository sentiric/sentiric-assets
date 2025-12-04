import os
import glob
from pydub import AudioSegment

# XTTS v2 Native Format
TARGET_RATE = 22050 
TARGET_CHANNELS = 1 # Mono

SPEAKERS_DIR = "docs/audio/speakers"

def optimize_audio():
    print(f"🔧 SENTIRIC AUDIO OPTIMIZER (XTTS v2 PREP)")
    print(f"🎯 Hedef: {TARGET_RATE}Hz Mono 16-bit WAV")
    
    wav_files = glob.glob(os.path.join(SPEAKERS_DIR, "**/*.wav"), recursive=True)
    
    if not wav_files:
        print("❌ Hiç .wav dosyası bulunamadı!")
        return

    for wav_path in wav_files:
        try:
            # Dosyayı yükle
            audio = AudioSegment.from_wav(wav_path)
            
            # Analiz
            needs_change = False
            if audio.frame_rate != TARGET_RATE: needs_change = True
            if audio.channels != TARGET_CHANNELS: needs_change = True
            
            if needs_change:
                print(f"   🔨 İşleniyor: {os.path.basename(wav_path)}")
                
                # Dönüştür
                audio = audio.set_frame_rate(TARGET_RATE)
                audio = audio.set_channels(TARGET_CHANNELS)
                
                # Normalize (Ses seviyesini eşitle -dBFS)
                target_dBFS = -20.0
                change_in_dBFS = target_dBFS - audio.dBFS
                audio = audio.apply_gain(change_in_dBFS)
                
                # Üzerine yaz (Export)
                audio.export(
                    wav_path, 
                    format="wav", 
                    parameters=["-acodec", "pcm_s16le"]
                )
            else:
                print(f"   ✅ Zaten uygun: {os.path.basename(wav_path)}")
                
        except Exception as e:
            print(f"   ❌ Hata: {wav_path} -> {e}")

    print("\n✨ Tüm referans sesler XTTS için optimize edildi.")

if __name__ == "__main__":
    optimize_audio()