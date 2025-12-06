```bash
cd ~/sentiric/sentiric-assets
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install google-genai
pip install google-genai --pre

export GEMINI_API_KEY="API_KEYİNİZ"
python tools/audio/google_harvester.py

```