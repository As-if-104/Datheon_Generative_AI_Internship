import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.prompts import build_prompt
from src.schema import Invoice

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.5-flash-lite"   


def extract_invoice(text):
    prompt = build_prompt(text)
    config = types.GenerateContentConfig(
        response_mime_type="application/json",  # ask for JSON only
        temperature=0,                          # 0 = more consistent answers
    )

    for attempt in range(1, 6):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            break
        except Exception as e:
            # Only retry when the server is busy; other errors stop here
            if "503" not in str(e) or attempt == 5:
                raise
            print(f"  Server busy, retrying ({attempt}/5)...")
            time.sleep(10)

    data = json.loads(response.text)   # text -> Python dictionary
    return Invoice(**data)             # validate with Pydantic