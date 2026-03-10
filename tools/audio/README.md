```bash
cd ~/sentiric/sentiric-assets
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install google-genai
pip install google-genai --pre
pip install pyyaml
export GEMINI_API_KEY=""
# python tools/audio/google_harvester.py
python tools/audio/announcements.py

```