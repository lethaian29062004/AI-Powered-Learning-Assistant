from google import genai
from google.genai import types

def generate_text(action, text, config):
    client = genai.Client(api_key=config["GEMINI_API_KEY"])
    model = config["MODEL"]

    if action == "summarize":
        prompt = f"Summarize this text:\n\n{text}"
    elif action == "explain":
        prompt = f"Explain simply for students:\n\n{text}"
    elif action == "questions":
        prompt = f"Make 5 practice questions based on this:\n\n{text}"
    else:
        prompt = text

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    return response.text

# Gemini API wrapper (clean separation).