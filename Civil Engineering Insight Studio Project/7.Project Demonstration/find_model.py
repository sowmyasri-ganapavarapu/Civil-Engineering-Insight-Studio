import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Searching for working model...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if '1.5' in m.name or 'flash' in m.name or 'pro' in m.name:
                print(f"Testing {m.name}...")
                try:
                    model = genai.GenerativeModel(m.name)
                    response = model.generate_content("Hi")
                    print(f"SUCCESS: {m.name}")
                    with open('working_model.txt', 'w') as f:
                        f.write(m.name)
                    break
                except Exception as e:
                    print(f"Failed {m.name}: {e}")
except Exception as e:
    print(f"Global error: {e}")
