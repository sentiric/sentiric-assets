from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("🔍 Google AI Modelleri Kontrol Ediliyor...\n")

models = client.models.list()

print("📋 TÜM MODELLER:")
print("-" * 50)

tts_models = []
for model in models:
    model_name = model.name.replace("models/", "")
    
    # Model bilgilerini göster
    print(f"\n📦 {model_name}")
    
    if hasattr(model, 'display_name'):
        print(f"   Display: {model.display_name}")
    
    if hasattr(model, 'description'):
        print(f"   Desc: {model.description[:100]}...")
    
    if hasattr(model, 'supported_generation_methods'):
        methods = model.supported_generation_methods
        if methods:
            print(f"   Methods: {', '.join(methods)}")
    
    # TTS modellerini topla
    if "tts" in model_name.lower():
        tts_models.append(model_name)

print(f"\n{'='*50}")
print(f"🎯 TOPLAM {len(tts_models)} TTS MODELİ:")
print("=" * 50)

for tts_model in tts_models:
    print(f"✅ {tts_model}")

print(f"\n💡 Kullanmanız gereken: gemini-2.5-flash-preview-tts")
print("   Dokümandaki örnekte bu model kullanılıyor.")