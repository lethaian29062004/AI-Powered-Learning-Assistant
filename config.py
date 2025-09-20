import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    GEMINI_API_KEY = "AIzaSyDVVGX2DTWbEcfaBEcdYpdbKNEMNrHiX9E"
    MODEL = "gemini-1.5-flash"

# Handles config (API key, debug mode).