from flask import Blueprint, render_template, request, jsonify
import google.genai as genai
from config import Config

#
main_bp = Blueprint("main", __name__)

# 
client = genai.Client(api_key=Config.GEMINI_API_KEY)


#
@main_bp.route("/") 
def index():
    return render_template("index.html")

#
@main_bp.route("/about")
def about():
    return render_template("about.html")

#
@main_bp.route("/process/<action>", methods=["POST"])
def process(action):
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400



#
    if action == "summarize":
        prompt = f"""
        Summarize this text in simple terms.
        Highlight the key points by wrapping them with **double asterisks**.
        Text: {text}
        """
    elif action == "explain":
        prompt = f"""
        Explain this text clearly for a student.
        Highlight the key terms or main ideas by wrapping them with **double asterisks**.
        Text: {text}
        """
    elif action == "questions":
        prompt = f"""
        Based on the following text, generate multiple-choice questions.
        For each question:
        - Start with 'Q1:', 'Q2:' etc.
        - Provide 4 answer options labeled A, B, C, D.
        - Clearly mark the correct answer at the end of each question in the format (Correct: X).
        Text: {text}
        """
    else:
        return jsonify({"error": "Unknown action"}), 400
    
 
#      

    try:
        response = client.models.generate_content(
            model=Config.MODEL,
            contents=prompt
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

# 
@main_bp.route("/process/topic", methods=["POST"])
def process_topic():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"Extract the main topic of this text in 1–3 words: {text}"

    try:
        response = client.models.generate_content(
            model=Config.MODEL,
            contents=prompt
        )
        return jsonify({"result": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
