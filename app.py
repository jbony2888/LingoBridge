from flask import Flask, request, jsonify, render_template
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")

# Initialize Google Translate client
translate_client = translate.Client()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect_language", methods=["POST"])
def detect_language():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Detect language using Google Translate
        result = translate_client.detect_language(user_message)
        detected_language = result["language"]
        print("Detected language from Google Translate:", detected_language)  # Log detected language

        return jsonify({"language": detected_language})

    except Exception as e:
        print("Error in language detection with Google Translate:", str(e))  # Log error details
        return jsonify({"error": f"Language detection failed: {str(e)}"}), 500

@app.route("/translate", methods=["POST"])
def translate_message():
    data = request.get_json()
    user_message = data.get("message")
    target_language = data.get("language")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Translate message using Google Translate
        translation = translate_client.translate(
            user_message, target_language=target_language
        )
        translated_text = translation["translatedText"]

        response_data = {
            "original_message": user_message,
            "translated_message": translated_text,
        }
        return jsonify(response_data)

    except Exception as e:
        print("Error in translation with Google Translate:", str(e))  # Log the exception details
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
